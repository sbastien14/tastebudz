import React from 'react';
import { PiStarFill, PiStarHalfFill, PiStar } from 'react-icons/pi';
import { Colors } from '../../data/Constants';
import ProfilePicture from '../../assets/testProfilePicture.jpeg';

function ReviewCard({ reviewer, comment, date }) {
  const randomRating = Math.random() * 5;
  const fullStars = Math.floor(randomRating);
  const halfStar = randomRating % 1 >= 0.5 ? 1 : 0;
  const emptyStars = 5 - fullStars - halfStar;

  const renderStars = () => {
    let stars = [];
    for (let i = 0; i < fullStars; i++) {
      stars.push(<PiStarFill size={30} key={`full-${i}`} />);
    }
    if (halfStar) {
      stars.push(<PiStarHalfFill size={30} key="half" />);
    }
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<PiStar size={30} key={`empty-${i}`} />);
    }
    return stars;
  };

  return (
    <div style={styles.reviewContainer}>
      <div>
        <div style={styles.rating}>{renderStars()}</div>
        <p style={styles.review}>{comment}</p>
        <div style={styles.reviewerTag}>
          <img src={ProfilePicture} style={styles.reviewerImg} alt='Reviewer' />
          <div style={styles.reviewerID}>
            <h3>{reviewer}</h3>
            <p>{date}</p>
          </div>
        </div>
      </div>
    </div>
  );
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