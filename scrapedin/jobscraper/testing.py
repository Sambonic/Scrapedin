import re
text = """Navier AI is a venture-backed startup building 1000x faster Computational Fluid Dynamics simulations using ML.

Why

Engineers today use simulation tools that are slow, expensive, and overly complex. Analysis teams are typically composed of PhDs with years of experience using esoteric software. This results in slow design iterations and performance left on the table.

Despite these performance and usability issues, simulations are crucial in modern engineering for everything from the design of hair dryers to rockets to F1 Cars.



At Navier AI, we believe the future of engineering is digital, in which fast, high-quality simulations drive the design of everything from aircraft to heatsinks. We are building advanced physics-ML models to enable fast physics simulators for simulation-driven design.

Our first product is a web app for fluid dynamics simulations and design optimization.



Navier AI is hiring a Frontend Engineer to build the next generation of engineering simulators. As a Frontend Engineer, you’ll work with the Founders on designing and developing an entirely new user experience for complex engineering tasks such as fluid simulations and structural analysis.





Bonus Points if you have





Navier AI was founded byand- Experienced Aerospace Engineers who’ve built and launched products at the world’s leading hardware companies like SpaceX, Tesla and Aurora."""

# Replace multiple whitespaces with a single space
text = re.sub(r'\s+', ' ', text)

# Remove extra empty lines
text = '\n'.join([line for line in text.splitlines() if line.strip()])
print(text)