import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set aesthetic styling for the ThreatLevel presentation
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#11111b", "figure.facecolor": "#11111b", "grid.color": "#31353c"})

print("Loading Machine Learning Models...")
model = joblib.load('final_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

print("Extracting NLP Features...")
# Get the hundreds of thousands of words the vectorizer learned
feature_names = vectorizer.get_feature_names_out()

# Get the mathematical weight the Logistic Regression assigned to each word
# For Logistic Regression, we look at the absolute coefficients!
importances = np.abs(model.coef_[0])

# Sort the features by how dangerous the model thinks they are
indices = np.argsort(importances)[::-1]

# We want to grab the Top 15 highest impact features
top_n = 15
top_indices = indices[:top_n]
top_features = [feature_names[i] for i in top_indices]
top_importances = importances[top_indices]

# Plotting the "Histogram" (Horizontal Bar Chart of Importance)
plt.figure(figsize=(12, 8))
# Create a cool gradient color map (Crimson/Mint colors)
colors = sns.color_palette("blend:#990000,#77dc7a", top_n)[::-1] 

ax = sns.barplot(x=top_importances, y=top_features, palette=colors)

plt.title('ThreatLevel NLP Model: Top Phishing Feature Indicators', fontsize=18, fontweight='bold', color='white', pad=20)
plt.xlabel('Logistic Regression Feature Importance (Absolute Coefficient)', fontsize=14, color='#c8c6c5')
plt.ylabel('Extracted Data Keyword (N-Gram)', fontsize=14, color='#c8c6c5')

# Add values on the bars
for i, v in enumerate(top_importances):
    ax.text(v + 0.001, i + 0.1, f"{v:.4f}", color='white', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('nlp_feature_histogram.png', dpi=300, bbox_inches='tight')
print("Successfully generated nlp_feature_histogram.png!")
