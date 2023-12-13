// GoogleSignInButton.js

import React from 'react';

function GoogleSignInButton({ onSuccess }) {
  window.onSignIn = function(googleUser) {
    const id_token = googleUser.getAuthResponse().id_token;
    onSuccess(id_token);
  }

  return (
    <div className="g-signin2" data-onsuccess="onSignIn"></div>
  );
}

export default GoogleSignInButton;
