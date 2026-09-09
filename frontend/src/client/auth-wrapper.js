const BACK_END_URL = import.meta.env.VITE_BACK_END_URL || "http://localhost:8080";

/**
 * Global Security Interceptor Loop
 */
async function enforceGlobalSecurityGuard() {
    // Only intercept pages that explicitly declare a protected layout context
    if (document.body.getAttribute("data-protected") !== "true") return;

    const token = localStorage.getItem("pvr_jwt");

    if (!token) {
        console.warn("PVR Security Guard: Access denied. Dropping token routing context.");
        window.location.href = "/";
        return;
    }

    try {
        const verifyResponse = await fetch(`${BACK_END_URL}/auth/me`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!verifyResponse.ok) throw new Error("Invalid session state");
        
        // Broadcast custom security event indicating it is safe to draw components
        document.dispatchEvent(new CustomEvent("pvr-auth-verified", { detail: { token } }));
    } catch (err) {
        console.error("PVR Security Guard: Session verification aborted. Redirecting.");
        localStorage.removeItem("pvr_jwt");
        window.location.href = "/";
    }
}

// Execute guard check immediately upon execution timeline evaluation
enforceGlobalSecurityGuard();
