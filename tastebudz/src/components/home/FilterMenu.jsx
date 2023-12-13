import React from 'react'
import { Dimensions, Colors } from '../../data/Constants'

function FilterMenu() {
  return (
    <div style={styles.filters}>
        <div style={styles.filterContainer}>
            <div>
                <h3 style={styles.filterHeader}>Cuisine</h3>
                <div style={styles.filterOptionsContainer}>
                    {/* <label style={styles.filterOption}>
                        <input type="checkbox"  style={styles.filterCheckbox}/>
                        Italian
                    </label>
                    <label style={styles.filterOption}>
                        <input type="checkbox" style={styles.filterCheckbox}/>
                        Mexican
                    </label>
                    <label style={styles.filterOption}>
                        <input type="checkbox" style={styles.filterCheckbox}/>
                        Chinese
                    </label>
                    <label style={styles.filterOption}>
                        <input type="checkbox" style={styles.filterCheckbox}/>
                        Ethopian
                    </label>
                    <label style={styles.filterOption}>
                        <input type="checkbox" style={styles.filterCheckbox}/>
                        Asian Fusion
                    </label>
                    <label style={styles.filterOption}>
                        <input type="checkbox" style={styles.filterCheckbox}/>
                        Steakhouse
                    </label> */}
                    <button style={styles.filterOption}>Italian</button>
                    <button style={styles.filterOption}>Mexican</button>
                    <button style={styles.filterOption}>Ethopian</button>
                    <button style={styles.filterOption}>Chinese</button>
                    <button style={styles.filterOption}>Thai</button>
                    <button style={styles.filterOption}>Steakhouse</button>
                </div>
                <div>
                    <h3 style={styles.filterHeader}>Distance</h3>
                    <label style={styles.distanceLabel} for="distance">5 mi</label>
                    <input style={styles.distance} type='range' name='distance' min={5} max={50}></input>
                    <label for="distance">50 mi</label>
                </div>
            </div>
           
        </div>
    </div>
  )
}

const styles = {
    filters: {
        width: '34rem',
        height: '34rem'
    },

    filterHeader: {
        fontSize: Dimensions.MEDIUM * 1.2,
        textTransform: 'uppercase',
        letterSpacing: 2,
        textAlign: 'left'
    },

    filterContainer: {
        display: 'flex',
        fontSize: Dimensions.SMALL,
        textTransform: 'uppercase',
        flexDirection: 'column',
        borderRadius: 5,
        height: '34rem',
        width: '34rem',
        fontWeight: 'bold',
        padding: '2rem',
        backgroundColor: '#F3F5F7',
        filter: `drop-shadow(-5px 5px ${Colors.SHADOW_GRAY})`,
        
    },

    filterOptionsContainer: {
        display: 'grid',
        gap: '2rem 5rem',
        gridAutoFlow: 'column',
        gridTemplateRows: '1fr 1fr',
        gridAutoColumns: '20%',
    },

    filterOption: {
        display: 'flex',
        justifyContent: 'center',
        width: 120,
        padding: 10,
        border: `2px solid ${Colors.PRIMARY}`,
        borderRadius: 25,
        alignItems: 'center',
        letterSpacing: 1,
        backgroundColor: 'white',
        color: Colors.PRIMARY,
        cursor: 'pointer'
    },

    distanceLabel: {
        marginRight: 20
    },

    distance: {
        width: '25rem',
        background: Colors.PRIMARY,
        marginRight: 20
    },

    filterCheckbox: {
        marginRight: 10,
        height: 20, 
        width: 20
    }
}

export default FilterMenu