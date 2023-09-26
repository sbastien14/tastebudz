import React from 'react'
import {Colors} from '../data/Constants'

function Button({buttonText, buttonStyle, buttonSize, buttonAction}) {

  return (
    <button style={{
        padding: '10px 30px',
        width: 'fit-content',
        textTransform: 'uppercase',
        letterSpacing: 2,
        fontWeight: 'bold',
        backgroundColor: 'white',
        color: Colors.PRIMARY,
        border:  `solid 3px ${Colors.PRIMARY}`,
        borderRadius: 3,
    }} onClick={buttonAction}>{buttonText}</button>
  )
}

export default Button