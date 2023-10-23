import React from 'react'
import {Colors} from '../../data/Constants'

function Button({buttonText, buttonStyle, buttonWidth, buttonHeight, buttonAction, onClick}) {

  return (
    <button style={{
        padding: '10px 30px',
        width: buttonWidth,
        height: buttonHeight,
        textTransform: 'uppercase',
        letterSpacing: 2,
        fontWeight: 'bold',
        backgroundColor: Colors.PRIMARY,
        cursor: 'pointer',
        color: 'white',
        border:  `solid 3px ${Colors.PRIMARY}`,
        borderRadius: 3,
    }} onClick={onClick}>{buttonText}</button>
  )
}

export default Button