// GoogleSignInButton.js
import GoogleButton from 'react-google-button'
import React from 'react';

function GoogleSignInButton({ onSuccess }) {
  let onSignIn = function(googleUser) {
    const id_token = googleUser.getAuthResponse().id_token;
    onSuccess(id_token);
  }


  return (
    <GoogleButton style= {styles.signIn}
  onClick={() => { onSignIn() }}
/>
  );
}
const styles = {
  signIn: {
      width: 500,
    },
}

export default GoogleSignInButton;
