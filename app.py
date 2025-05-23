from flask import Flask, send_file, abort
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

@app.route('/plot/<int:n>')
def dynamic_plot(n):
    if n <= 0 or n > 99999:
        abort(400, description="Invalid plot index")

    try:
        np.random.seed(n)
        fig, axs = plt.subplots(3, 3, figsize=(15, 12))
        fig.suptitle(f"Stress Test Plot #{n}", fontsize=18)

        x = np.linspace(0, 10, 500)

        # 1. Noisy high-frequency sine
        y1 = np.sin(x * (n % 50 + 1)) + np.random.normal(0, 0.5, size=x.shape)
        axs[0, 0].plot(x, y1, label="High Freq Sin", color='darkblue')
        axs[0, 0].legend()

        # 2. Large bar chart with long tail
        bars = np.random.zipf(a=2.0, size=50)
        axs[0, 1].bar(range(len(bars)), bars, color='darkorange')
        axs[0, 1].set_title("Zipf Bars")

        # 3. Dense scatter with colormap
        x2 = np.random.randn(1000)
        y2 = np.random.randn(1000)
        axs[0, 2].scatter(x2, y2, c=np.sin(x2 + y2), cmap='plasma', alpha=0.7)
        axs[0, 2].set_title("Dense Scatter")

        # 4. Random walk with outliers
        walk = np.cumsum(np.random.randn(500))
        walk[::50] += np.random.randn(10) * 50  # add outliers
        axs[1, 0].plot(walk, color='red')
        axs[1, 0].set_title("Random Walk with Spikes")

        # 5. Heatmap with NaN
        data = np.random.randn(20, 20)
        if n % 7 == 0:
            data[5:10, 5:10] = np.nan  # inject NaNs
        im = axs[1, 1].imshow(data, cmap='coolwarm')
        fig.colorbar(im, ax=axs[1, 1])
        axs[1, 1].set_title("Heatmap with NaN")

        # 6. Line plot with discontinuity
        y3 = np.tan(x - 5)  # creates vertical asymptotes
        y3[np.abs(y3) > 100] = np.nan  # clip extreme jumps
        axs[1, 2].plot(x, y3, color='green')
        axs[1, 2].set_title("Discontinuous tan(x)")

        # 7. Text-heavy subplot
        for i in range(20):
            axs[2, 0].text(0.1, i * 0.5, f"Label {i}: seed={n}", fontsize=8)
        axs[2, 0].set_xlim(0, 5)
        axs[2, 0].set_ylim(0, 20)
        axs[2, 0].set_title("Text Load")

        # 8. Polar plot (edge rendering case)
        theta = np.linspace(0, 2 * np.pi, 400)
        r = 1 + 0.5 * np.sin(n * theta % 5)
        axs[2, 1] = fig.add_subplot(3, 3, 8, projection='polar')
        axs[2, 1].plot(theta, r, color='purple')
        axs[2, 1].set_title("Polar Curve")

        # 9. Empty or failed plot occasionally
        if n % 29 == 0:
            axs[2, 2].axis('off')
        else:
            axs[2, 2].hist(np.random.randn(100), bins=20, color='gray')
        axs[2, 2].set_title("Histogram or Empty")

        # Layout, save, return
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        return send_file(buf, mimetype='image/png')

    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)