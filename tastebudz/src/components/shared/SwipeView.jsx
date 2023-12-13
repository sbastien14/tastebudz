import React from 'react'
import { Dimensions, Colors } from '../../data/Constants'
import {BsArrowLeft, BsArrowRight} from 'react-icons/bs'
import {PiStarFill, PiStarHalfFill} from 'react-icons/pi'
import ReviewCard from '../../components/shared/ReviewCard'
import testRestaurantImg from '../../assets/testRestaurantImg.jpeg'

function SwipeView() {
    let testMap = [1,2,3]
    return (
    <div style={styles.swipeView}>
        <button style={styles.swipeAction}><BsArrowLeft color='white'/></button>
        <div style={styles.swipeContainer}>
            <div style={styles.restaurantCard}>
                <div style={styles.restaurantHeader}>
                    <h3 style={styles.restaurantName}>Pastabilities</h3>
                    <div>
                        <PiStarFill  size={30}/>
                        <PiStarFill size={30}/>
                        <PiStarFill size={30}/>
                        <PiStarFill  size={30}/>
                        <PiStarHalfFill size={30}/>
                    </div>
                </div>                            
                <div style={styles.restaurantImgContainer}></div>
                <div style={styles.restaurantInfo}>
                    <h4>311 S Franklin St, Syracuse NY 13202</h4>
                    <p>Italian</p>
                    <p style={styles.expenses}>$$</p>
                </div>
            </div>
            <div style={styles.restaurantReviews}>
                {
                    testMap.map((review) => (
                        <ReviewCard/>
                    ))
                }
            </div>
        </div>
        <button style={styles.swipeAction}><BsArrowRight color='white'/></button>
    </div>
    )
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
        background: `url(${testRestaurantImg})`,
        backgroundPosition: 'center center'
    },

    expense: {
        fontWeight: 'bold'
    }



}

export default SwipeView