import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Dimensions, Colors } from '../../data/Constants';
import { BsArrowLeft, BsArrowRight } from 'react-icons/bs';
import { PiStarFill, PiStarHalfFill } from 'react-icons/pi';
import ReviewCard from '../../components/shared/ReviewCard';

function SwipeView() {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [restaurants, setRestaurants] = useState([]);

    useEffect(() => {
        // Fetch restaurant data 
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/dataset');
                setRestaurants(response.data);
            } catch (error) {
                console.error('Error fetching restaurant data:', error);
            }
        };

        fetchData();
    }, []);

    const handleSwipeLeft = () => {
        setCurrentIndex(prevIndex => prevIndex > 0 ? prevIndex - 1 : restaurants.length - 1);
    };

    const handleSwipeRight = () => {
        setCurrentIndex(prevIndex => (prevIndex + 1) % restaurants.length);
    };

    if (restaurants.length === 0) {
        return <div>Loading restaurants...</div>;
    }

    const currentRestaurant = restaurants[currentIndex];

    return (
        <div style={styles.swipeView}>
            <button style={styles.swipeAction} onClick={handleSwipeLeft}>
                <BsArrowLeft color='white'/>
            </button>
            <div style={styles.swipeContainer}>
                <div style={styles.restaurantCard}>
                    <div style={styles.restaurantHeader}>
                        <h3 style={styles.restaurantName}>{currentRestaurant.name}</h3>
                        <div>
                            {[...Array(Math.floor(currentRestaurant.rating))].map((_, i) => (
                                <PiStarFill key={i} size={30} />
                            ))}
                            {currentRestaurant.rating % 1 > 0 && <PiStarHalfFill size={30} />}
                        </div>
                    </div>
                    <div style={{ ...styles.restaurantImgContainer, backgroundImage: `url(${currentRestaurant.imageUrl})` }}>
                        {/* Image should display here */}
                    </div>
                    <div style={styles.restaurantInfo}>
                        <h4>{currentRestaurant.address}</h4>
                        <p>{currentRestaurant.type}</p>
                        <p style={styles.expenses}>{currentRestaurant.priceRange || '$$'}</p>
                    </div>
                </div>
                <div style={styles.restaurantReviews}>
                    {currentRestaurant.reviews.map((review, index) => (
                        <ReviewCard key={index} reviewer={review.reviewer} comment={review.comment} />
                    ))}
                </div>
            </div>
            <button style={styles.swipeAction} onClick={handleSwipeRight}>
                <BsArrowRight color='white'/>
            </button>
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
        // Image background set here 
    },

    expenses: {
        fontWeight: 'bold'
    }
}

export default SwipeView;
