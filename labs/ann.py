# %% Imports
from sklearn.datasets import fetch_openml

mnist = fetch_openml("mnist_784", version=1)
X = mnist.data.astype("float32")  # shape (70000, 784)
y = mnist.target.astype("int64")  # shape (70000,)


# %%
sns.heatmap(X[0].reshape(28, 28), cbar=False, cmap="gray")
plt.axis("off")
plt.gca().set_aspect("equal", adjustable="box")
plt.tight_layout()
