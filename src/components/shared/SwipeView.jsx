import React, { useState } from 'react';
import { Dimensions, Colors } from '../../data/Constants';
import { BsArrowLeft, BsArrowRight } from 'react-icons/bs';
import { PiStarFill, PiStarHalfFill } from 'react-icons/pi';
import ReviewCard from '../../components/shared/ReviewCard';
import dinosaurBBQImg from '../../assets/syracuse-exterior-960x639.jpg';
import pastabilitiesImg from '../../assets/image-asset.jpg';
import kittyHoynesImg from '../../assets/1393511327089.jpg';

const restaurantData = [
    {
        name: "Pastabilities",
        type: "Italian",
        address: "311 S Franklin St, Syracuse NY 13202",
        rating: 4.5,
        reviews: [
            { reviewer: "Alice Johnson", comment: "Amazing homemade pasta!" },
            { reviewer: "John Smith", comment: "Loved the cozy atmosphere and delicious food." },
            { reviewer: "Emily White", comment: "Best Italian restaurant in Syracuse." },
        ],
        imageUrl: pastabilitiesImg
    },
    {
        name: "Dinosaur BBQ",
        type: "Barbecue",
        address: "246 W Willow St, Syracuse, NY 13202",
        rating: 4.2,
        reviews: [
            { reviewer: "David Brown", comment: "Great BBQ, loved the ribs!" },
            { reviewer: "Sarah Johnson", comment: "A must-visit for BBQ lovers." },
            { reviewer: "Mike Davis", comment: "Friendly staff and fantastic brisket." },
        ],
        imageUrl: dinosaurBBQImg
    },
    {
        name: "Kitty Hoynes Irish Pub",
        type: "Irish",
        address: "301 W Fayette St, Syracuse, NY 13202",
        rating: 4.3,
        reviews: [
            { reviewer: "Patrick O'Brien", comment: "Authentic Irish pub with a great selection of beers." },
            { reviewer: "Molly Malone", comment: "Perfect spot for a cozy evening." },
            { reviewer: "Liam Gallagher", comment: "The fish and chips were outstanding!" },
        ],
        imageUrl: kittyHoynesImg
    },
];

function SwipeView() {
    const [currentIndex, setCurrentIndex] = useState(0);

    const handleSwipeLeft = () => {
        setCurrentIndex((prevIndex) => prevIndex > 0 ? prevIndex - 1 : restaurantData.length - 1);
    };

    const handleSwipeRight = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % restaurantData.length);
    };

    const currentRestaurant = restaurantData[currentIndex];

    return (
        <div style={styles.swipeView}>
            <button style={styles.swipeAction} onClick={handleSwipeLeft}><BsArrowLeft color='white'/></button>
            <div style={styles.swipeContainer}>
                <div style={styles.restaurantCard}>
                    <div style={styles.restaurantHeader}>
                        <h3 style={styles.restaurantName}>{currentRestaurant.name}</h3>
                        <div>
                            <PiStarFill size={30} />
                            <PiStarFill size={30} />
                            <PiStarFill size={30} />
                            <PiStarFill size={30} />
                            <PiStarHalfFill size={30} />
                        </div>
                    </div>
                    <div style={{ ...styles.restaurantImgContainer, background: `url(${currentRestaurant.imageUrl}) center center / cover no-repeat` }}>
                        {/* Image will be displayed here */}
                    </div>
                    <div style={styles.restaurantInfo}>
                        <h4>{currentRestaurant.address}</h4>
                        <p>{currentRestaurant.type}</p>
                        <p style={styles.expenses}>$$</p>
                    </div>
                </div>
                <div style={styles.restaurantReviews}>
                    {currentRestaurant.reviews.map((review, index) => (
                        <ReviewCard key={index} reviewer={review.reviewer} comment={review.comment} />
                    ))}
                </div>
            </div>
            <button style={styles.swipeAction} onClick={handleSwipeRight}><BsArrowRight color='white'/></button>
        </div>
    );
}

const styles = {
    swipeView: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: 'white',
        padding: 50,
        flex: 3,
        gap: 50
    },

    swipeContainer: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'space-around',
        gap: 50
    },

    swipeAction: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: 150,
        width: 150,
        fontSize: 50,
        borderRadius: 180,
        border: 'none',
        filter: `drop-shadow(-5px 5px ${Colors.SHADOW_GRAY})`,
        backgroundColor: Colors.SECONDARY,
        cursor: 'pointer'
    },

    restaurantCard: {
        height: '60rem',
        backgroundColor: Colors.GRAY,
        border: `2px solid ${Colors.GRAY}`,
        filter: `drop-shadow(0px 3px ${Colors.SHADOW_GRAY}) drop-shadow(0px -2px ${Colors.SHADOW_GRAY})`,
        borderRadius: 25,
    },

    restaurantHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 20,
    },

    restaurantInfo: {
        padding: 20,
        fontSize: Dimensions.SMALL,
        textTransform: 'uppercase',
        letterSpacing: 1,
    },

    restaurantReviews: {
        display: 'flex',
        gap: 50
    },

    restaurantName: {
        fontSize: Dimensions.MEDIUM
    },

    restaurantImgContainer: {
        height: 650,
        // Image background set dynamically
    },

    expenses: {
        fontWeight: 'bold'
    }
}

export default SwipeView;
