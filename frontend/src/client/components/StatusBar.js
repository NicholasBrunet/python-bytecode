export class StatusBar {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    render(statusText = "Ready") {
        if (!this.container) return;
        this.container.innerHTML = `
            <div style="height: 22px; background: #007acc; font-size: 12px; color: #fff; display: flex; align-items: center; padding: 0 10px; justify-content: space-between;">
                <div id="status-left">${statusText}</div>
                <div>Python 3.12 • UTF-8</div>
            </div>
        `;
    }
    
    updateStatus(newText) {
        const target = this.container.querySelector("#status-left");
        if (target) target.textContent = newText;
    }
}
