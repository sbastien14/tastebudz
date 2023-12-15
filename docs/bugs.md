# Bug Tracker
This is a bug tracking document with all bugs faced through the development process as well as their status.

<style>
    .new {
        margin: 0;
        padding: 0.3rem 0.5rem;
        border-radius: 1.0rem;
        color: white;
        background-color: tomato;
    }
    .open {
        margin: 0;
        padding: 0.3rem 0.5rem;
        border-radius: 1.0rem;
        color: white;
        background-color: orange;
    }
    .fixed {
        margin: 0;
        padding: 0.3rem 0.5rem;
        border-radius: 1.0rem;
        color: black;
        background-color: yellow;
    }
    .retest {
        margin: 0;
        padding: 0.3rem 0.5rem;
        border-radius: 1.0rem;
        color: white;
        background-color: mediumslateblue;
    }
    .closed {
        margin: 0;
        padding: 0.3rem 0.5rem;
        border-radius: 1.0rem;
        color: black;
        background-color: lightgreen;
    }
</style>

| Bug | Status | Description |
| :--: | :--: | :-- |
| getUser Parameter | <p class="new">New</p> | Parameter for username is provided but not used. Instead, returns currently logged-in user. |
| UI Responsiveness | <p class="new">New</p> | Sizing on different displays and accessibility is not functioning. |
| Delete User Account Unauthorized | <p class="open">Open</p> | Supabase API returns 401 unauthorized and does not delete user account. This operation requires a service role, but this was added and did not resolve the issue. |
| API Receives OPTIONS Only | <p class="closed">Closed</p> | Frontend sent requests using axios module to backend. Backend only received OPTIONS. This was a CORS error that was resolved on the backend side through a setting in the Connexion module. |
| Create User Profile Parameter | <p class="closed">Closed</p> | Username parameter is supplied but operation uses currently logged-in user instead. |
| Invalid OAuth Provider Requested | <p class="closed">Closed<p> |Backend API returns 500 error on invalid provider instead of intended 400 error. |
| Invalid Login | <p class="closed">Closed</p> | Backend API returns 502 error on invalid credentials instead of intended 400 error. |