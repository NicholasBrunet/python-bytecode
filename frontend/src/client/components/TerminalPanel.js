export class TerminalPanel {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.isDragging = false;
    }

    render() {
        if (!this.container) return;

        this.container.innerHTML = `
            <div id="terminal-resizer" style="height: 4px; background: transparent; cursor: ns-resize; transition: background 0.2s;"></div>
            <div style="height: 35px; background: #1e1e1e; display: flex; align-items: center; padding: 0 20px; font-size: 12px; font-weight: bold; color: #858585; border-bottom: 1px solid #3c3c3c;">
                TERMINAL
            </div>
            <pre id="terminal-log-output" style="flex: 1; padding: 12px; font-family: 'Fira Code', monospace; font-size: 13px; color: #33ff33; overflow-y: auto; white-space: pre-wrap; margin: 0;">PVR Environment mounted. System secure...</pre>
        `;

        this.logOutput = this.container.querySelector("#terminal-log-output");
        this.setupResizeMechanics();
    }

    writeLog(message) {
        if (this.logOutput) {
            this.logOutput.textContent += `\n${message}`;
            this.logOutput.scrollTop = this.logOutput.scrollHeight;
        }
    }

    setupResizeMechanics() {
        const resizer = this.container.querySelector("#terminal-resizer");
        
        resizer.addEventListener("hover", () => resizer.style.background = "#007acc");
        resizer.addEventListener("mousedown", (e) => {
            this.isDragging = true;
            document.body.style.cursor = "ns-resize";
            e.preventDefault();
        });

        window.addEventListener("mousemove", (e) => {
            if (!this.isDragging) return;
            const newHeight = window.innerHeight - e.clientY;
            if (newHeight >= 40 && newHeight <= window.innerHeight - 100) {
                this.container.style.height = `${newHeight}px`;
            }
        });

        window.addEventListener("mouseup", () => {
            if (this.isDragging) {
                this.isDragging = false;
                document.body.style.cursor = "default";
            }
        });
    }
}
