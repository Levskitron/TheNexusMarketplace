import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import Listing  # Assuming a model file is used
from database import db  # Assuming a database setup
from forms import logoutForm, CreateListingForm, DeleteListingForm, BuyListingForm

home_bp = Blueprint('home', __name__)

UPLOAD_FOLDER = 'static/listingPhotos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to validate file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@home_bp.route('/home')
def home_page():

    if not session.get('username'):
        return redirect(url_for('auth.login'))

    username = session['username']
    logout_form=logoutForm()
    BuyListForm = BuyListingForm()
    CLForm = CreateListingForm()
    DelListForm = DeleteListingForm()
    if not session.get('username'):
        return redirect(url_for('auth.login'))
    listings = Listing.query.all()

    is_admin = session.get('privilege') == '1'

    return render_template('home.html', listings=listings, logout_form=logout_form, CLForm=CLForm, username=username, DelListForm=DelListForm, BuyListForm=BuyListForm)

@home_bp.route('/create_listing', methods=['POST'])
def create_listing():
    CLForm = CreateListingForm()

    if not session.get('username'):
        return redirect(url_for('auth.login'))

    if CLForm.validate_on_submit():
        name = CLForm.title.data
        description = CLForm.description.data
        price = CLForm.price.data
        file = request.files.get('image')  # Use .get() for safety

        filepath = None  # Default in case no image is uploaded

        # Check if file is uploaded and valid
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
            else:
                flash('Invalid file type. Please upload a JPG, PNG, JPEG, or GIF image.')
                return redirect(url_for('home.home_page'))

        # Create the new listing, image is optional
        new_listing = Listing(
            name=name,
            description=description,
            price=float(price),
            image_url=filepath,
            username=session['username']
        )
        db.session.add(new_listing)
        db.session.commit()
        flash('Listing created successfully!')
        return redirect(url_for('home.home_page'))
    else:
        flash('Form validation failed. Please check your input.')
        return redirect(url_for('home.home_page'))
    
@home_bp.route('/delete_listing/<int:listing_id>', methods=['POST'])
def delete_listing(listing_id):

    DelListForm = DeleteListingForm()

    if not session.get('username'):
        return redirect(url_for('auth.login'))

    # Query the listing
    listing = Listing.query.get_or_404(listing_id)


    # Check if the user is the owner of the listing or has admin privilege (privilege=1)
    #if session['username'] != listing.username and session.get('privilege') != 1:  # Check privilege 1 for admin
    #    flash('You do not have permission to delete this listing.')
    #    return redirect(url_for('home.home_page'))

    # Get the file path of the image
    image_filepath = listing.image_url  # Assuming image_url is stored with the full path like 'static/ListingPhotos/filename.jpg'
    
    # Delete the file from the filesystem
    if os.path.exists(image_filepath):
        os.remove(image_filepath)
    
    # Delete the listing from the database
    db.session.delete(listing)
    db.session.commit()

    flash('Listing and associated image deleted successfully.')
    return redirect(url_for('home.home_page', DelListForm=DelListForm))

# Added Buy Listing Route
@home_bp.route('/buy_listing/<int:listing_id>', methods=['POST'])
def buy_listing(listing_id):

    BuyListForm = BuyListingForm()

    # Ensure the user is logged in
    if not session.get('username'):
        flash("You must be logged in to buy a listing.")
        return redirect(url_for('auth.login'))

    # Fetch the listing
    listing = Listing.query.get_or_404(listing_id)

    # Ensure the listing is still available (not sold)
    if listing.is_sold:
        flash("This listing has already been sold.")
        return redirect(url_for('home.home_page'))  # Adjust this as per your listings route

    # Mark the listing as sold and record the buyer
    listing.is_sold = True
    listing.buyer_username = session['username']
    db.session.commit()

    # Flash a success message
    flash(f"Congratulations! You have successfully bought the listing: {listing.name}.")
    return redirect(url_for('home.home_page', BuyListForm=BuyListForm))  # Redirect back to listings page

@home_bp.route('/support')
def support():
    return render_template('support.html')

@home_bp.route('/sponsor')
def sponsor():
    return render_template('sponsor.html')