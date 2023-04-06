# Solving Nonlinear Equations System
Course work in the discipline "Basics of Programming" on the topic "Solving systems of nonlinear equations". The program solves the given systems using appropriate methods and provides graphical data on the solution. The PyQt5 and matplotlib modules are used for the graphical interface.

This work is devoted to the development of software for solving systems of nonlinear equations using object-oriented programming. The task of the software is to display the solution of a system of two nonlinear equations in text and graphical form and to write it to a file if necessary.

The input data for this work is the chosen type of system, the chosen solution method (the Jacobi or Gauss-Seidel method), the minimum calculation accuracy, and the system of two nonlinear equations itself, which is given in the appropriate form.

Using the drop-down list titled "Select the type of equations" by clicking on this list and selecting the appropriate type, you need to select the type of equations to be processed by the program.

![image](https://user-images.githubusercontent.com/89355159/230402760-e0433c25-c177-4934-a752-a0e3fa1962a1.png)

After selecting the type of equations, the window displays the selected type of equations, fields for entering coefficients, and the corresponding variables near these fields. Next, by clicking on the list of methods, you need to select the method that will be 
to be processed by the program (by default, it is the method of simple iteration (Jacobi)), and enter all the necessary values in the fields: accuracy, coefficients, initial 
approximations.

![image](https://user-images.githubusercontent.com/89355159/230403049-80256000-de3d-4a28-ae3e-69c9af208304.png)

To solve the entered system, click the "Solve" button, after which a warning will be displayed, which must be corrected to solve the system, or a solution with iterations and a graph. A window will also appear asking if you want to save the solution to a file.

![image](https://user-images.githubusercontent.com/89355159/230403249-f0758eb7-57f5-497b-8af7-79f33f5e06d8.png)

