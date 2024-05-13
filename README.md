[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
    </li>
   <li>
      <a href="#demo-scripts">Demo Scripts</a>
      <ul>
        <li><a href="#object-transformations-lighting-and-shading">Object Transformations, Lighting and Shading</a></li>
        <li><a href="#hello-world">Complex Shading (Hello World)</a></li>
        <li><a href="#dynamic-mesh-manipulation">Dynamic Meshes</a></li>
      </ul>
   </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
# About The Project

**GLPG (PygletPlayground) is a Python package that provides basic and easy to 
use OpenGL functionalities for interactive 3D scenes. It is completely 
based on the [pyglet](https://pyglet.org/) library.**

### Some Features:
- ***3D Models***
    - triangle mesh model import
    - Intuitive model transformations
- ***Shading***
  - Configurable light objects
  - Multiple light sources 
  - GLSL shader import
- ***Texturing***
  - Texture import from image
  - Texture wrapping
  - Multiple textures for one model

### Built With

[![Bootstrap][Python.badge]][Python-url]
[![Bootstrap][OpenGL.badge]][OpenGL-url]
[![Bootstrap][Pyglet.badge]][Pyglet-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTALLATION -->
# Installation
To install the package via pip run
```sh
pip install glpg
```

or, to run the demo scripts, clone the repository
```sh
git clone https://github.com/flowmeadow/pygletPlayground.git
```
 
and install the required packages
```sh
pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Demo Scripts

## Object Transformations, Lighting and Shading
### How To:
From the project's root as current working directory execute this:
```sh
python demo_scripts/demo_object_transform.py
```
### YouTube:

[![GLPG Demo 1](https://img.youtube.com/vi/r7DSk9WGdD0/0.jpg)](https://www.youtube.com/watch?v=r7DSk9WGdD0 "GLPG Demo 1")

https://www.youtube.com/watch?v=r7DSk9WGdD0

## Complex Shading (Hello World)
### How To:
From the project's root as current working directory execute this:
```sh
python demo_scripts/demo_hello_world.py
```
### YouTube:

[![GLPG Demo 1](https://img.youtube.com/vi/uEExaj8HDHk/0.jpg)](https://www.youtube.com/watch?v=uEExaj8HDHk "GLPG Demo 1")

https://www.youtube.com/watch?v=uEExaj8HDHk

## Dynamic Meshes
### How To:
From the project's root as current working directory execute this:
```sh
python demo_scripts/demo_height_map.py
```
### YouTube:

[![GLPG Demo 1](https://img.youtube.com/vi/4bAnUes0nGI/0.jpg)](https://www.youtube.com/watch?v=4bAnUes0nGI "GLPG Demo 1")

https://www.youtube.com/watch?v=4bAnUes0nGI

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.rst` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/badge/License-MIT-<COLOR>?style=for-the-badge
[license-url]: https://github.com/flowmeadow/pygletPlayground/blob/e45b61bddf8b22932f94ca77957ece683284a3dd/LICENSE.rst
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/florian-wiese-155527a4/
[Python.badge]: https://img.shields.io/static/v1?message=Python&logo=python&color=1182c3&logoColor=white&label=%20&style=for-the-badge
[Python-url]: https://www.python.org/
[OpenGL.badge]: https://img.shields.io/static/v1?message=OpenGL&logo=opengl&color=1182c3&logoColor=white&label=%20&style=for-the-badge
[OpenGL-url]: https://www.opengl.org/
[OpenCV.badge]: https://img.shields.io/static/v1?message=OpenCV&logo=opencv&color=1182c3&logoColor=white&label=%20&style=for-the-badge
[OpenCV-url]: https://opencv.org/
[Pyglet.badge]: https://img.shields.io/static/v1?message=pyglet&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAADQAAAA0CAYAAADFeBvrAAAABHNCSVQICAgIfAhkiAAACFtJREFUaIHtmluMXlUVx%2F%2Frm85ML1BaikTAQkupVEQqxSZGEsBobIoVXghpIOCLqfCgiVEjYKISAy9gCEYx2hhfeEAtCNFEAdsSCOHaYmmgFSmIFVsQemGYby7f3uvnw9nnY%2FfMd50ZCA%2Bu5CRnn7PX5b%2F32muvvc6R%2Fk%2F9E2CAfRC6ZlVJMvpkSWslrZK0UtKJwPFmZpJGJB2StE%2FSHknPSDpoZsymHTOiNPofB34E7AQa9Eju3nD3XcDNwKoPahbbARkC1gEPAaGNwcdQF3AB2A6sB4ana1ffI5JG8TxJt0v6QjsZgAMv1Wq1VyrPF0laLWmOpEEzq1XeI2mbmd0oaYeZeb829kzAPOAm4N1WM5G1cff7gLkdZJ0HXO%2FuD7r7WIsZHAV%2BDCx4v8AsAx7MQQDR3Q%2BFEDaHEJ7I3h0EPtmH7DOAG9x9PxArwLYCK2YbzCrghcqsjMQYfzk2NrYcOM3dXyvfxRjvnqaexTHGu9z9SAXUHuD82QTzcsW99gKXZ30uz97XG43GJTPUebG776644T%2F7mfV2gpflM%2BPuHmPcAZye94sxbs7A7qQSpSjW3snAqelaAgx10X1qCGE7x0bQPcBZ0wUzL18zQIgx3jM2NnZ6pd984NESc4zxF%2Bm5jY%2BPnxlj%2FB6wNXcjd38duB%2B4Ajiugw1zgd9UQD0MnNAvGKOIZs2ZCSE8Ccyv9q3X66fFGN8uuwJXJ0M2ufsbdKAUDbcByzoNbAjhsYr73QrU2vG0ErKaLDTHGA9ScbOs7%2FJSl7tH4OoY4%2BYu%2B2gV2BPAxzrYs9Tdn8tYRoELegUzlKa1nJyREMLlHfqfmRk2GkJ4Oo18k9%2Fd%2Fwx8Hbg2XT9w9xfTAJSDdg8tPCDTc6G7H8p0bQXm9QJoHYXrlEHg1136NwFNHXh%2FodFofKkN30nu%2FqcSlLuPhRCu6qQrxvgz0j6VXPDL3cAYRW5WWvQGbVwt41mW8rAqmH3AeZ146%2FX6UnfPo%2BhWOuRxFNFxf6%2F9RZE1h2wEfthxBJISd3%2Bpgma822hn%2FBvdvZH4jtIhQKT%2B381mqQGsyd9XI8VVkgbS%2FaSk3%2FVgU13SgcqznQMDA1t64JWkZ83sLUkys4WSlnfp%2F1vgaOo%2FR9LG%2FGUTEEUWfVn27kkz29PNGjMbM7O%2F5M%2BAe81sshuvJE1MTAiOOd%2Bt7KLvX5Iezx6tA%2BaUjXyGTpb0qWQQZnZ%2FLwYleqjSXgkMtOxZoeHh4WEVR4mS%2Ft2Nx8x%2BD5THinMkfbR8lwNamwkOIYSdvRiUOp9YUXi1pK91AwUMuPtGSSel9rikv%2Feg8llJ46WMZPsU4d%2FJFvVoTzH%2BPd7rWoTtEeDG8fHxFa2AHT58eBFwnbu%2Fk%2FHcS5ccryR3P5zx3Vg%2Bz6d6ZTIOSa%2BZ2VivgNrQcZJuHRoa%2BhbwTIzxWUmlzLkUR%2B01aWEDjJjZbb2uPUnPS7oo3a8oVomRA2q6jZm9Ol0UwLuS%2Fmtmy5Osj0i61Mwu7cAzYmbfVFEF6onM7FDWXKyiFFAkeBQb6vHTAdCCXg8hXOXum4G3OnWkqBDtiDFeKeluM4vT1LlQqbbRnKFUN5sWxRgnBgaay2Th4ODgYUnXNxqNnw8MDGwws8%2BriKKLJAVJbwL%2FqNVqWyQ9Pjg42BF4D9S0fY4kmRnASLrvG5i7%2Fy0DNCRpfhrtXem6BViowjWCpIO1Wm26s9GKRiQhHRu2mz5JUWrqmQYHBw8Bb6bmkhjjlM3RzN4xs9fM7PUZuFaTgMVZ84haAHo5u1%2Fdp%2FwjZSAxM5nZZ6dlZX%2BU27ivLCfngJppjpnN6ZYp52RmR919W9a%2BmPernqaicGNm5X6FMttzQM8AITEMSrqwHyUplZ9IzXNjjF%2BZgc3daC2piJlSoKnhPoXuXVm28GA%2FGoAF7v5Ixv80%2FRYzeiR33%2FKeGn8hTUBLo27ODBoDzuhHUQjhGncfT%2FwhxnhHW2WJ6vX6acC5FPW%2F8mqb%2FlDUF94u0QC3txUOrCpPn6nzDf0AAua7%2B%2F3ZoNRjjD8FTm3HMzo6er6773X3A9m1293%2FUIlkpY5v815ZKwBTE9Oss1XcZn8roV1Ane3FN59SRnD3vTHG709OTq4hK4QAC0IIV7j7f7JEs6wvfJXK9yJgEfBq5m6P0eGDQMm0nlQkAWKM8a5%2BACUZq1IFNTcSdz%2Fi7i8De9x9D7DP3SepUJqdKdl%2BjPFOji2StK1G5cYMA9sy4e%2BEEDZMA9SZ7n5fuaZ6JXc%2FMDExMaWG3Wg0vlipvj7SCnQ7Y9amM1HJvJsO66CDnAXAend%2FoHLuyQGMu%2FuTFGejXcA3mOpqp7j7UxlbHfhcP4bUKD42lUo9LfbO%2Ftpe3jxgeQjhSmBTecUYNwFrSOG90WhcRCXUA3NDCA%2FnRUngDno84ueC5gN%2FzYQEisJ5zyfZmRJFjfxXHFta206fgSoXuILiE0YTlLv%2FEVg6y7a30n1KCOHhCpi9wNkzFfxpio9Nufs912g01s2S7VMoBYCnsjKxpy2ktwJ9N6LYyfOZwt2PplrzkllRUuhZFGO8sxLNypmZHTCZsrPcPV9TUOwJ%2BynKsx1r4F1kL6XIAF6l8tE4heeZuVkHxScAt%2BQhvQTm7ofS%2BroWOKcHWauAa9x9S8rNqgX%2FOkU06ysATOfHi5qk8yXdJumSqgzAzWwcmJT0fKU6U540V5vZEDC38uMFFGXhR83sJklPzcbptiei2Fs2UPxH0PLXmB7J0zoJ7v4ocBkf4NbQCtgwcAFwG7AbaCQDuwJJA%2FEi8BOgeWibCc3272VzJJ0i6TOSPuHuZ9VqtcUqqqhGUVA8LOkVSS%2BqqFEfMLPGbNnwvv7ORZGTlZdUnP%2F5UP0f92Gn%2FwEPfsFPUDopZwAAAABJRU5ErkJggg%3D%3D&color=1182c3&logoColor=white&label=%20&style=for-the-badge
[Pyglet-url]: https://pyglet.org/
