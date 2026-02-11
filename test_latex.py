import streamlit as st

st.title("LaTeX Rendering Test")

# Test different LaTeX formats
st.write("## Test 1: st.markdown() with LaTeX")
st.markdown("The sine of theta is $\\sin(\\theta)$ and the fraction is $\\frac{1}{2}$")

st.write("## Test 2: st.latex() for display math")
st.latex(r"\sin(\theta) = \frac{opposite}{hypotenuse}")

st.write("## Test 3: st.write() with LaTeX")
st.write("Using st.write: $\\cos(30^\\circ) = \\frac{\\sqrt{3}}{2}$")

st.write("## Test 4: Raw string in markdown")
text = r"The equation is $\sin^2(\theta) + \cos^2(\theta) = 1$"
st.markdown(text)

st.write("## Test 5: Unicode math symbols")
st.markdown("Using Unicode: sin(θ) = ½ and angle 30°")
