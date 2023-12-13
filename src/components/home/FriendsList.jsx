import React from 'react';
import { Colors, Dimensions } from '../../data/Constants';
import ProfilePicture from '../../assets/testProfilePicture.jpeg';

function FriendsList() {
    const testFriendsList = [
        { name: 'John Doe', username: '@DoeboyJohn' },
        { name: 'Emily Clark', username: '@EClark' },
        { name: 'David Brown', username: '@DavidBr' },
        { name: 'Sarah Johnson', username: '@SJWorld' },
        // Add more friends here
    ];

    return (
        <div style={styles.friendsListContainer}>
            <h3 style={styles.friendHeader}>Friends</h3>
            {
                testFriendsList.map((friend, index) => (
                    <div key={index} style={styles.userID}>
                        <img style={styles.userImg} src={ProfilePicture} alt={friend.name} />
                        <div style={styles.userTag}>
                            <h3>{friend.name}</h3>
                            <p>{friend.username}</p>
                        </div>
                    </div>
                ))
            }
        </div>
    );
}

const styles = {
    friendsListContainer: {
        display: 'flex',
        flexDirection: 'column',
        flex: 0.7,
        width: '38rem',
        borderRadius: 5,
        backgroundColor: Colors.GRAY,
        filter: `drop-shadow(-5px 5px ${Colors.SHADOW_GRAY})`,
        // additional styling
    },
    friendHeader: {
        fontSize: Dimensions.MEDIUM * 1.2,
        textTransform: 'uppercase',
        letterSpacing: 2,
        textAlign: 'left',
        padding: '10px 2rem',
        // additional styling
    },
    userImg: {
        marginRight: 20,
        width: 65,
        height: 65, 
        borderRadius: '100%', 
        objectFit: 'cover',
        // additional styling
    },
    userID: {
        display: 'flex',
        alignItems: 'center',
        textTransform: 'uppercase',
        letterSpacing: 2,
        lineHeight: 0.5,
        padding: '1rem 2rem',
        borderTop: `2px solid ${Colors.SHADOW_GRAY}`,
        cursor: 'pointer',
        '&:hover': {
            backgroundColor: Colors.PRIMARY, // Change as needed
            color: 'white', // Change as needed
        },
        // additional styling
    },
    userTag: {
        // additional styling
    }
};

export default FriendsList;
