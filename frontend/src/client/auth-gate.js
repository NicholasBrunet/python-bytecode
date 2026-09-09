// 🔒 LOCKING DOWN YOUR EXACT ENV VARIABLE CONTEXT SCHEME
const BACK_END_URL = import.meta.env.VITE_BACK_END_URL || "http://localhost:8080";

/**
 * Executes the login evaluation loop and redirect handling mechanics
 */
async function runAuthorizationGatePipeline() {
    const urlParams = new URLSearchParams(window.location.search);
    let token = localStorage.getItem("pvr_jwt");

    // 1. Intercept incoming tokens from Microsoft SSO redirects
    if (urlParams.has("access_token")) {
        token = urlParams.get("access_token");
        localStorage.setItem("pvr_jwt", token);
        console.log("PVR Auth Gate: New token captured from SSO channel.");
    }

    // 2. If no token is found in memory, bounce the browser directly to the Microsoft login endpoint
    if (!token) {
        updateAuthDisplayMessage("Redirecting to Microsoft SSO...");
        window.location.href = `${BACK_END_URL}/auth/login`;
        return;
    }

    // 3. Token exists -> Verify it with your backend container context before navigating
    try {
        updateAuthDisplayMessage("Validating active runtime token context...");
        
        const verifyCheck = await fetch(`${BACK_END_URL}/auth/me`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!verifyCheck.ok) throw new Error("Token state expired");

        // Verification successful! Natively jump to the workspace file layout
        updateAuthDisplayMessage("Access granted. Initializing workspace layout...");
        window.location.href = "/panel";

    } catch (err) {
        // Token is broken, missing, or falsified -> Wipe local storage data and force re-login
        console.warn("PVR Auth Gate: Session invalid or expired. Cycling auth stream.");
        localStorage.removeItem("pvr_jwt");
        updateAuthDisplayMessage("Session invalid. Re-routing to login portal...");
        window.location.href = `${BACK_END_URL}/auth/login`;
    }
}

/**
 * Quick visual element update helper
 */
function updateAuthDisplayMessage(message) {
    const textNode = document.getElementById("auth-status");
    if (textNode) {
        textNode.textContent = message;
    }
}

// Fire the authorization gate immediately upon script module load evaluation
runAuthorizationGatePipeline();
