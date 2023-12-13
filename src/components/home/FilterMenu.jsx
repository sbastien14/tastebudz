import React, { useState } from 'react';
import { Dimensions, Colors } from '../../data/Constants';

function FilterMenu() {
  const [selectedCuisines, setSelectedCuisines] = useState([]);

  const handleCuisineClick = (cuisine) => {
    if (selectedCuisines.includes(cuisine)) {
      setSelectedCuisines(selectedCuisines.filter(item => item !== cuisine));
    } else {
      setSelectedCuisines([...selectedCuisines, cuisine]);
    }
  };

  const cuisines = ['Italian', 'Mexican', 'Ethiopian', 'Chinese', 'Thai', 'Steakhouse'];

  return (
    <div style={styles.filters}>
      <div style={styles.filterContainer}>
        <div>
          <h3 style={styles.filterHeader}>Cuisine</h3>
          <div style={styles.filterOptionsContainer}>
            {cuisines.map((cuisine) => (
              <button 
                key={cuisine} 
                style={selectedCuisines.includes(cuisine) ? { ...styles.filterOption, backgroundColor: Colors.PRIMARY, color: 'white' } : styles.filterOption}
                onClick={() => handleCuisineClick(cuisine)}>
                {cuisine}
              </button>
            ))}
          </div>
          <div>
            <h3 style={styles.filterHeader}>Distance</h3>
            <label style={styles.distanceLabel}>5 mi</label>
            <input style={styles.distance} type='range' name='distance' min={5} max={50}></input>
            <label>50 mi</label>
          </div>
        </div>
      </div>
    </div>
  );
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