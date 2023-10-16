import React from 'react'
import {PiStarFill, PiStarHalfFill} from 'react-icons/pi'
import { Colors } from '../../data/Constants'
import ProfilePicture from '../../assets/testProfilePicture.jpeg'

function ReviewCard() {
  return (
    <div style={styles.reviewContainer}>
        <div>
            <div style={styles.rating}>
                <PiStarFill  size={30}/>
                <PiStarFill size={30}/>
                <PiStarFill size={30}/>
                <PiStarFill size={30}/>
                <PiStarHalfFill size={30}/>
            </div>
            <p style={styles.review}>Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur, sint nemo eveniet ipsum veritatis hic consectetur commodi consequuntur dolore quam quas adipisci. Aspernatur vitae facilis voluptatum nihil ea libero. Labore.</p>
            <div style={styles.reviewerTag}>
                <img src={ProfilePicture} style={styles.reviewerImg}  alt='Reviewer'/>
                <div style={styles.reviewerID}>
                    <h3>John Doe</h3>
                    <p>Jan. 4th 2017</p>
                </div>
            </div>
        </div>
    </div>
  )
}

const styles = {
    reviewContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        width: '27rem',
        backgroundColor: Colors.SECONDARY,
        textTransform: 'uppercase',
        // color: Colors.ACCENT,
        fontSize: 20,
        padding: '2rem',
        borderRadius: 10,
        filter: `drop-shadow(-5px 5px ${Colors.SHADOW_GRAY})`,
        
    },

    review: {
        lineHeight: 1.7,
        fontWeight: 'bold',
    },

    reviewerID: {
        letterSpacing: 2,
        lineHeight: 0.3
    },

    reviewerTag: {
        textTransform: 'uppercase',
        display: 'flex',
        alignItems: 'center'
    },

    reviewerImg: {
        marginRight: 20,
        width: 65,
        height: 65, 
        borderRadius: '100%', 
        objectFit: 'cover'        
    }


}

export default ReviewCard