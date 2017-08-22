/**
 * Created by yuecao on 8/21/17.
 */
function countdown (callback, duration, message) {
    // If no message is provided, we use an empty string
    message = message || "";
    // Get reference to container, and set initial content
    var container = $('#message').html(duration + message);
    // Get reference to the interval doing the countdown
    var countdown = setInterval(function () {
        // If seconds remain
        if (--duration) {
            // Update our container's message
            container.html(duration + message);
            // Otherwise
        } else {
            // Clear the countdown interval
            clearInterval(countdown);
            // And fire the callback passing our container as `this`
            callback.call(container);
        }
        // Run interval every 1000ms (1 second)
    }, 1000);
};

// Use p.countdown as container, pass redirect, duration, and optional message

countdown(redirect, 5, " seconds ...");

// Function to be called after 5 seconds
function redirect() {
    // this.html("Redirecting to my profile...");
    window.location = "/profile/";
}
