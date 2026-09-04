# BCS-203 - Object Oriented Programming
## Detailed Step-Wise Solutions — Units I–IV (Combined)

## Detailed Step-Wise Solutions — UNIT I: Introduction to OOP principles and Core Java
### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: OOP Principles | Type: Theory | Difficulty: Basic]**  
**Question:** What are the four main principles of Object-Oriented Programming?  

*Concept from scratch:* Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects". The four main principles of OOP are:  

1. **Encapsulation:** This principle refers to the bundling of data (attributes) and methods (functions) that operate on the data into a single unit known as a class. It restricts direct access to some of the object's components and can prevent the accidental modification of data.  

2. **Abstraction:** Abstraction is the concept of hiding the complex reality while exposing only the necessary parts. It helps in reducing programming complexity and increases efficiency.  

3. **Inheritance:** This principle allows a new class, known as a subclass, to inherit properties and behaviors (methods) from an existing class, referred to as a superclass. This promotes code reusability and establishes a relationship between classes.  

4. **Polymorphism:** Polymorphism allows methods to do different things based on the object it is acting upon. It enables a single interface to represent different underlying forms (data types).  

*Result:* The four main principles of OOP are Encapsulation, Abstraction, Inheritance, and Polymorphism.

---

**Q2. [Unit I | Topic: Data Types | Type: Theory | Difficulty: Basic]**  
**Question:** Define primitive and reference data types in Java.  

*Concept from scratch:* In Java, data types are divided into two categories:  

1. **Primitive Data Types:** These are the most basic data types provided by Java. They represent single values and are not objects. The eight primitive data types in Java are:
   - `int`: for integers (e.g., 10)
   - `double`: for floating-point numbers (e.g., 10.5)
   - `char`: for characters (e.g., 'A')
   - `boolean`: for true/false values
   - `byte`, `short`, `long`, and `float` are also primitive types with various sizes.
   
2. **Reference Data Types:** These types refer to objects or instances of classes. They do not store the actual data but rather a reference (or address) to the data in memory. Examples include:
   - Strings
   - Arrays
   - User-defined classes (objects)

*Result:* In Java, primitive data types are basic types like int and boolean, while reference data types refer to objects and arrays.

---

**Q3. [Unit I | Topic: Inheritance | Type: Theory | Difficulty: Basic]**  
**Question:** Explain the concept of inheritance with an example.  

*Concept from scratch:* Inheritance is a mechanism in OOP that allows a new class to inherit properties and behaviors from an existing class. The class that is inherited from is called the superclass (or parent class), and the class that inherits is called the subclass (or child class). This promotes code reusability and establishes a hierarchical relationship between classes.  

*Example:*  

```java
// Superclass
class Animal {
    void eat() {
        System.out.println("This animal eats food.");
    }
}

// Subclass
class Dog extends Animal {
    void bark() {
        System.out.println("The dog barks.");
    }
}

public class TestInheritance {
    public static void main(String[] args) {
        Dog myDog = new Dog();
        myDog.eat(); // Inherited method
        myDog.bark(); // Dog’s own method
    }
}
```

*Result:* In the example, `Dog` inherits the `eat` method from the `Animal` superclass, demonstrating inheritance.

---

### Section B: Computational & Applied Problems

**Q1. [Unit I | Topic: Control Statements | Type: Applied | Difficulty: Intermediate]**  
**Question:** Write a Java program that demonstrates the use of if-else and switch-case statements.  

*Concept from scratch:* Control statements in Java allow you to control the flow of execution of your program. The `if-else` statement is used for conditional execution, while `switch-case` provides a more readable way to execute different blocks of code based on the value of a variable.  

```java
import java.util.Scanner;

public class ControlStatementsDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a number (1-3): ");
        int number = scanner.nextInt();

        // Using if-else
        if (number == 1) {
            System.out.println("You entered one.");
        } else if (number == 2) {
            System.out.println("You entered two.");
        } else if (number == 3) {
            System.out.println("You entered three.");
        } else {
            System.out.println("Invalid number.");
        }

        // Using switch-case
        switch (number) {
            case 1:
                System.out.println("You selected one.");
                break;
            case 2:
                System.out.println("You selected two.");
                break;
            case 3:
                System.out.println("You selected three.");
                break;
            default:
                System.out.println("Invalid selection.");
                break;
        }
        scanner.close();
    }
}
```

*Result:* The program demonstrates both `if-else` and `switch-case` statements based on user input.

---

**Q2. [Unit I | Topic: Arrays | Type: Applied | Difficulty: Intermediate]**  
**Question:** Create a program that takes an array of integers as input and returns the sum and average of the elements.  

*Concept from scratch:* Arrays in Java are used to store multiple values of the same type in a single variable. To calculate the sum and average, you can iterate through the array elements, accumulate the sum, and then divide by the number of elements for the average.  

```java
import java.util.Scanner;

public class ArraySumAverage {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the number of elements: ");
        int n = scanner.nextInt();
        int[] numbers = new int[n];

        // Input elements
        for (int i = 0; i < n; i++) {
            System.out.print("Enter element " + (i + 1) + ": ");
            numbers[i] = scanner.nextInt();
        }

        // Calculate sum and average
        int sum = 0;
        for (int number : numbers) {
            sum += number;
        }
        double average = (double) sum / n;

        System.out.println("Sum: " + sum);
        System.out.println("Average: " + average);
        scanner.close();
    }
}
```

*Result:* The program computes the sum and average of user-input integers from an array.

---

**Q3. [Unit I | Topic: Constructors | Type: Applied | Difficulty: Intermediate]**  
**Question:** Write a class with a constructor that initializes an object with values passed as parameters and displays those values.  

*Concept from scratch:* A constructor is a special method used to initialize objects. It is called when an object of a class is created and can take parameters to set initial values for the object's attributes.  

```java
class Person {
    String name;
    int age;

    // Constructor
    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }
}

public class ConstructorDemo {
    public static void main(String[] args) {
        Person person1 = new Person("Alice", 30);
        Person person2 = new Person("Bob", 25);

        person1.display(); // Output: Name: Alice, Age: 30
        person2.display(); // Output: Name: Bob, Age: 25
    }
}
```

*Result:* The program demonstrates a class with a constructor that initializes and displays the object attributes.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit I | Topic: Packages and Interfaces | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the importance of packages and interfaces in Java with examples.  

*Concept from scratch:*  
- **Packages:** In Java, packages are used to group related classes and interfaces together. They help in organizing classes, preventing naming conflicts, and controlling access with access modifiers. A package can be created using the `package` keyword.  
- **Interfaces:** An interface in Java is a reference type, similar to a class, that can contain only constants, method signatures, default methods, static methods, and nested types. Interfaces allow you to define a contract that classes can implement, promoting a form of multiple inheritance and loose coupling.

*Example of Package:*

```java
package com.example.shapes;

public class Circle {
    public void draw() {
        System.out.println("Drawing a Circle");
    }
}
```

*Example of Interface:*

```java
interface Drawable {
    void draw(); // abstract method
}

class Rectangle implements Drawable {
    public void draw() {
        System.out.println("Drawing a Rectangle");
    }
}
```

*Result:* Packages help organize code, while interfaces enable abstraction and multiple inheritance in Java.

---

**Q2. [Unit I | Topic: String Handling | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain different methods of the String class and illustrate their use with code snippets.  

*Concept from scratch:* The `String` class in Java provides various methods to manipulate strings. Some commonly used methods include:
- `length()`: Returns the length of the string.
- `charAt(int index)`: Returns the character at the specified index.
- `substring(int beginIndex, int endIndex)`: Returns a substring from the string.
- `toLowerCase()` and `toUpperCase()`: Converts the string to lower or upper case.
- `indexOf(String str)`: Returns the index of the first occurrence of the specified substring.

*Example:*

```java
public class StringMethodsDemo {
    public static void main(String[] args) {
        String str = "Hello, World!";
        
        System.out.println("Length: " + str.length()); // Length: 13
        System.out.println("Character at index 7: " + str.charAt(7)); // Character at index 7: W
        System.out.println("Substring: " + str.substring(7, 12)); // Substring: World
        System.out.println("Lowercase: " + str.toLowerCase()); // Lowercase: hello, world!
        System.out.println("Index of 'World': " + str.indexOf("World")); // Index of 'World': 7
    }
}
```

*Result:* The code demonstrates various string methods and their outputs.

---

**Q3. [Unit I | Topic: Inheritance | Type: Numerical | Difficulty: Advanced]**  
**Question:** Create a superclass and subclass in Java. Implement method overriding and demonstrate its functionality.  

*Concept from scratch:* Method overriding occurs when a subclass provides a specific implementation of a method that is already defined in its superclass. This allows for dynamic method dispatch, enabling the Java runtime to decide which method to execute based on the object's actual type.  

*Example:*

```java
class Animal {
    void sound() {
        System.out.println("Animal makes a sound");
    }
}

class Cat extends Animal {
    void sound() {
        System.out.println("Cat meows");
    }
}

public class InheritanceDemo {
    public static void main(String[] args) {
        Animal myAnimal = new Animal(); // Animal reference and object
        Animal myCat = new Cat(); // Animal reference but Cat object

        myAnimal.sound(); // Output: Animal makes a sound
        myCat.sound();    // Output: Cat meows (method overriding)
    }
}
```

*Result:* The example demonstrates method overriding in inheritance with different outputs based on the object type.

---

## Detailed Step-Wise Solutions — UNIT II: Exception Handling and Multithreading
### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: Exception Handling | Type: Theory | Difficulty: Basic]**  
**Question:** What is exception handling in Java, and why is it important?  

*Concept from scratch:* Exception handling in Java is a powerful mechanism to handle runtime errors, allowing the normal flow of the program to continue. It is important because it provides a way to manage errors gracefully, ensuring that the program does not crash unexpectedly. Java uses the `try`, `catch`, `finally`, and `throw` keywords to handle exceptions.

*Result:* Exception handling is crucial for maintaining program stability and providing user-friendly error messages.

---

**Q2. [Unit II | Topic: Multithreading | Type: Theory | Difficulty: Basic]**  
**Question:** Define multithreading and its advantages.  

*Concept from scratch:* Multithreading is a Java feature that allows concurrent execution of two or more threads in a single program. Each thread can run independently, which helps in utilizing CPU resources efficiently. Advantages include:
- Improved application performance through parallelism.
- Better resource utilization.
- Simplified program structure for certain tasks, like GUI applications.

*Result:* Multithreading enhances performance and resource management in Java applications.

---

**Q3. [Unit II | Topic: AWT | Type: Theory | Difficulty: Basic]**  
**Question:** What is AWT, and how does it differ from Swing?  

*Concept from scratch:* AWT (Abstract Window Toolkit) is the original package for creating graphical user interfaces (GUIs) in Java. AWT components are heavyweight and rely on the native system for rendering, which can lead to platform-specific behavior. Swing, on the other hand, is built on AWT and provides a richer set of lightweight components that are more flexible and platform-independent.

*Result:* AWT is the foundational GUI toolkit, while Swing offers enhanced capabilities and better cross-platform compatibility.

---

### Section B: Computational & Applied Problems

**Q1. [Unit II | Topic: Exception Handling | Type: Applied | Difficulty: Intermediate]**  
**Question:** Write a program that uses try-catch blocks to handle division by zero.  

*Concept from scratch:* The `try-catch` block in Java can be used to catch exceptions that may occur during the execution of a program. If an exception occurs, the code in the `catch` block will execute, allowing you to handle the error gracefully instead of crashing the program.  

```java
import java.util.Scanner;

public class DivisionByZero {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter numerator: ");
        int numerator = scanner.nextInt();
        System.out.print("Enter denominator: ");
        int denominator = scanner.nextInt();

        try {
            int result = numerator / denominator;
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Error: Division by zero is not allowed.");
        } finally {
            scanner.close();
        }
    }
}
```

*Result:* The program handles division by zero gracefully by catching the `ArithmeticException`.

---

**Q2. [Unit II | Topic: Multithreading | Type: Applied | Difficulty: Intermediate]**  
**Question:** Create a multithreaded Java application that prints numbers from 1 to 10 in one thread and letters A to J in another thread.  

*Concept from scratch:* In Java, you can create threads by extending the `Thread` class or implementing the `Runnable` interface. Each thread runs independently, allowing for concurrent execution.  

```java
class NumberThread extends Thread {
    public void run() {
        for (int i = 1; i <= 10; i++) {
            System.out.println(i);
            try {
                Thread.sleep(100); // Sleep for 100 milliseconds
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

class LetterThread extends Thread {
    public void run() {
        for (char c = 'A'; c <= 'J'; c++) {
            System.out.println(c);
            try {
                Thread.sleep(100); // Sleep for 100 milliseconds
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

public class MultithreadingDemo {
    public static void main(String[] args) {
        NumberThread numThread = new NumberThread();
        LetterThread letterThread = new LetterThread();

        numThread.start(); // Start the number thread
        letterThread.start(); // Start the letter thread
    }
}
```

*Result:* The program demonstrates multithreading by concurrently printing numbers and letters.

---

**Q3. [Unit II | Topic: I/O | Type: Applied | Difficulty: Intermediate]**  
**Question:** Implement a Java program that reads from a file and writes its content to another file.  

*Concept from scratch:* Java provides classes for file I/O operations, allowing you to read data from files and write data to files. The `FileReader` and `FileWriter` classes can be used for reading and writing character files, respectively.  

```java
import java.io.*;

public class FileCopy {
    public static void main(String[] args) {
        String sourceFile = "source.txt";
        String destinationFile = "destination.txt";

        try (BufferedReader reader = new BufferedReader(new FileReader(sourceFile));
             BufferedWriter writer = new BufferedWriter(new FileWriter(destinationFile))) {
             
            String line;
            while ((line = reader.readLine()) != null) {
                writer.write(line);
                writer.newLine();
            }
            System.out.println("File copied successfully!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

*Result:* The program reads content from `source.txt` and writes it to `destination.txt`.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit II | Topic: Networking | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the concepts of sockets and server sockets in Java networking.  

*Concept from scratch:* Sockets are endpoints for sending and receiving data across a network. In Java, the `Socket` class represents a client-side socket, while the `ServerSocket` class is used for creating server-side sockets. A server socket listens for incoming client requests on a specific port, while a client socket connects to a server socket using an IP address and port number.

*Result:* Sockets allow for communication between clients and servers in Java networking applications.

---

**Q2. [Unit II | Topic: Event Handling | Type: Theory | Difficulty: Advanced]**  
**Question:** Describe the event handling mechanism in AWT with an example.  

*Concept from scratch:* In AWT, event handling is a mechanism that allows the program to respond to user actions such as mouse clicks, key presses, etc. It involves three main components: event source, event listener, and event object. The event source generates an event, the listener listens for that event, and when the event occurs, the listener is notified.

*Example:*

```java
import java.awt.*;
import java.awt.event.*;

public class EventHandlingDemo {
    public static void main(String[] args) {
        Frame frame = new Frame("Event Handling Example");
        Button button = new Button("Click Me");

        button.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                System.out.println("Button Clicked!");
            }
        });

        frame.add(button);
        frame.setSize(300, 200);
        frame.setLayout(new FlowLayout());
        frame.setVisible(true);

        frame.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent we) {
                System.exit(0);
            }
        });
    }
}
```

*Result:* The code demonstrates event handling in AWT by printing a message when the button is clicked.

---

**Q3. [Unit II | Topic: AWT Controls | Type: Numerical | Difficulty: Advanced]**  
**Question:** Develop a Java GUI application using AWT that includes various controls like buttons, text fields, and labels.  

*Concept from scratch:* AWT provides a set of components, or controls, that can be used to create user interfaces. Common controls include buttons, text fields, labels, checkboxes, and more. You can handle events from these controls to make your application interactive.

*Example:*

```java
import java.awt.*;
import java.awt.event.*;

public class AWTControlsDemo {
    public static void main(String[] args) {
        Frame frame = new Frame("AWT Controls Example");
        Label label = new Label("Enter your name:");
        TextField textField = new TextField(20);
        Button button = new Button("Submit");

        button.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                System.out.println("Hello, " + textField.getText() + "!");
            }
        });

        frame.add(label);
        frame.add(textField);
        frame.add(button);
        frame.setSize(300, 200);
        frame.setLayout(new FlowLayout());
        frame.setVisible(true);

        frame.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent we) {
                System.exit(0);
            }
        });
    }
}
```

*Result:* The application demonstrates the use of AWT controls by greeting the user based on the input name.

---

## Detailed Step-Wise Solutions — UNIT III: Java Swing and JDBC
### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: Java Swing | Type: Theory | Difficulty: Basic]**  
**Question:** What is Java Swing, and how does it enhance GUI development?  

*Concept from scratch:* Java Swing is a set of APIs for providing a graphical user interface (GUI) for Java applications. Swing is built on top of AWT and offers a richer set of components, providing better functionality and flexibility. Swing components are lightweight, meaning they are not dependent on the native OS for their rendering.

*Result:* Swing enhances GUI development by providing a comprehensive set of lightweight components that are consistent across platforms.

---

**Q2. [Unit III | Topic: JDBC | Type: Theory | Difficulty: Basic]**  
**Question:** Define JDBC and its role in database connectivity.  

*Concept from scratch:* JDBC (Java Database Connectivity) is an API that enables Java applications to interact with various databases. It provides methods for querying and updating data in relational databases. JDBC allows developers to execute SQL statements, retrieve results, and manage database connections.

*Result:* JDBC is essential for enabling database connectivity in Java applications.

---

**Q3. [Unit III | Topic: RMI | Type: Theory | Difficulty: Basic]**  
**Question:** Explain Remote Method Invocation (RMI) in Java.  

*Concept from scratch:* RMI is a Java API that allows an object running in one Java virtual machine to invoke methods on an object running in another Java virtual machine. RMI uses a client-server architecture and facilitates remote communication between objects over a network.

*Result:* RMI enables remote method invocation in distributed Java applications.

---

### Section B: Computational & Applied Problems

**Q1. [Unit III | Topic: Swing Applet | Type: Applied | Difficulty: Intermediate]**  
**Question:** Create a simple Swing application with a button that changes the text of a label when clicked.  

*Concept from scratch:* Swing allows the creation of GUI applications using various components. The `JButton` and `JLabel` classes are commonly used to create interactive applications. An `ActionListener` can be added to the button to respond to click events.

*Example:*

```java
import javax.swing.*;
import java.awt.event.*;

public class SwingAppletDemo {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Swing Example");
        JButton button = new JButton("Click Me");
        JLabel label = new JLabel("Initial Text");

        button.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                label.setText("Text Changed!");
            }
        });

        frame.add(button);
        frame.add(label);
        frame.setLayout(new FlowLayout());
        frame.setSize(300, 200);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
```

*Result:* The application changes the label text when the button is clicked.

---

**Q2. [Unit III | Topic: JDBC Connectivity | Type: Applied | Difficulty: Intermediate]**  
**Question:** Write a program to connect to a database and retrieve records from a table using JDBC.  

*Concept from scratch:* JDBC provides a standard interface for database connectivity. You need to load the JDBC driver, establish a connection, create a statement, and execute queries to retrieve data from the database.

*Example:*

```java
import java.sql.*;

public class JDBCExample {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/mydatabase";
        String username = "root";
        String password = "password";

        try (Connection conn = DriverManager.getConnection(url, username, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM mytable")) {
             
            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("id") + ", Name: " + rs.getString("name"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

*Result:* The program connects to a MySQL database and retrieves records from a table.

---

**Q3. [Unit III | Topic: Remote Database Connectivity | Type: Applied | Difficulty: Intermediate]**  
**Question:** Demonstrate how to perform a remote database query using JDBC.  

*Concept from scratch:* To perform remote database queries, ensure that the database server is accessible over the network. The JDBC URL will specify the remote server's IP address and port. Follow similar steps as in local connectivity.

*Example:*

```java
import java.sql.*;

public class RemoteJDBCExample {
    public static void main(String[] args) {
        String url = "jdbc:mysql://192.168.1.100:3306/mydatabase"; // Remote IP
        String username = "remoteUser";
        String password = "remotePassword";

        try (Connection conn = DriverManager.getConnection(url, username, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM mytable")) {
             
            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("id") + ", Name: " + rs.getString("name"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

*Result:* The program demonstrates querying a remote database using JDBC.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit III | Topic: Java SQL Package | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the classes provided by the Java SQL package and their functionalities.  

*Concept from scratch:* The `java.sql` package provides classes and interfaces for accessing and processing data stored in a database. Key classes include:
- `DriverManager`: Manages a list of database drivers.
- `Connection`: Represents a connection to a specific database.
- `Statement`: Used to execute SQL queries.
- `PreparedStatement`: Extends `Statement` for executing precompiled SQL queries.
- `ResultSet`: Represents the result set of a query.

*Result:* The `java.sql` package is essential for database interaction in Java applications.

---

**Q2. [Unit III | Topic: Swing Components | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the use of tabbed panes in Swing applications with an example.  

*Concept from scratch:* A `JTabbedPane` allows users to switch between different panels (tabs) in a Swing application. It organizes multiple panels into a single container, providing a clean user interface.

*Example:*

```java
import javax.swing.*;

public class TabbedPaneExample {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Tabbed Pane Example");
        JTabbedPane tabbedPane = new JTabbedPane();

        JPanel panel1 = new JPanel();
        panel1.add(new JLabel("Content of Tab 1"));
        tabbedPane.addTab("Tab 1", panel1);

        JPanel panel2 = new JPanel();
        panel2.add(new JLabel("Content of Tab 2"));
        tabbedPane.addTab("Tab 2", panel2);

        frame.add(tabbedPane);
        frame.setSize(400, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
```

*Result:* The example demonstrates the use of tabbed panes to organize content in a Swing application.

---

**Q3. [Unit III | Topic: JDBC/ODBC Bridge | Type: Numerical | Difficulty: Advanced]**  
**Question:** Illustrate how to use the JDBC/ODBC bridge to connect to a Microsoft Access database.  

*Concept from scratch:* The JDBC-ODBC bridge allows Java applications to connect to ODBC data sources. This requires setting up an ODBC Data Source Name (DSN) on your system.

*Example:*

```java
import java.sql.*;

public class AccessDatabaseExample {
    public static void main(String[] args) {
        String url = "jdbc:odbc:myAccessDB"; // DSN name for MS Access
        String username = ""; // No username for Access
        String password = ""; // No password for Access

        try (Connection conn = DriverManager.getConnection(url, username, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM mytable")) {
             
            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("id") + ", Name: " + rs.getString("name"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

*Result:* The code demonstrates connecting to a Microsoft Access database using the JDBC-ODBC bridge.

---

## Detailed Step-Wise Solutions — UNIT IV: Java Beans and Servlets
### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Java Beans | Type: Theory | Difficulty: Basic]**  
**Question:** Define Java Beans and their purpose in Java development.  

*Concept from scratch:* Java Beans are reusable software components that follow specific conventions, such as providing a no-argument constructor, allowing properties to be set and retrieved through getter and setter methods. They are used for encapsulating data and providing a standard way to handle properties in Java applications.

*Result:* Java Beans are used to create reusable components in Java applications.

---

**Q2. [Unit IV | Topic: JAR Files | Type: Theory | Difficulty: Basic]**  
**Question:** What are JAR files, and how are they used in Java applications?  

*Concept from scratch:* JAR (Java Archive) files are packages that bundle multiple Java class files, associated metadata, and resources (such as images and text files) into a single file. JAR files are used for distributing Java applications, libraries, and components, making it easier to manage dependencies.

*Result:* JAR files simplify the distribution and deployment of Java applications.

---

**Q3. [Unit IV | Topic: Servlets | Type: Theory | Difficulty: Basic]**  
**Question:** What is a servlet, and what role does it play in web applications?  

*Concept from scratch:* A servlet is a Java class that runs on a web server and processes client requests and generates dynamic content. Servlets are used to handle HTTP requests and responses, allowing developers to create dynamic web applications by generating HTML content and managing user sessions.

*Result:* Servlets are essential for creating dynamic web applications in Java.

---

### Section B: Computational & Applied Problems

**Q1. [Unit IV | Topic: Developing a Bean | Type: Applied | Difficulty: Intermediate]**  
**Question:** Create a simple Java Bean with properties and methods and demonstrate how to access it.  

*Concept from scratch:* A Java Bean must have private properties, a no-argument constructor, and public getter and setter methods. This encapsulation allows the properties to be accessed and modified safely.

*Example:*

```java
public class PersonBean {
    private String name;
    private int age;

    // No-argument constructor
    public PersonBean() {}

    // Getter and Setter methods
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}

public class BeanDemo {
    public static void main(String[] args) {
        PersonBean person = new PersonBean();
        person.setName("Alice");
        person.setAge(30);

        System.out.println("Name: " + person.getName());
        System.out.println("Age: " + person.getAge());
    }
}
```

*Result:* The example demonstrates creating and accessing a simple Java Bean.

---

**Q2. [Unit IV | Topic: Bound Properties | Type: Applied | Difficulty: Intermediate]**  
**Question:** Implement an example of a Java Bean using bound properties.  

*Concept from scratch:* Bound properties allow listeners to be notified when a property changes. You can use the `PropertyChangeSupport` class to manage bound properties.

*Example:*

```java
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

public class BoundPersonBean {
    private String name;
    private PropertyChangeSupport support;

    public BoundPersonBean() {
        support = new PropertyChangeSupport(this);
    }

    public void setName(String name) {
        String oldName = this.name;
        this.name = name;
        support.firePropertyChange("name", oldName, name);
    }

    public String getName() {
        return name;
    }

    public void addPropertyChangeListener(PropertyChangeListener pcl) {
        support.addPropertyChangeListener(pcl);
    }
}

public class BoundBeanDemo {
    public static void main(String[] args) {
        BoundPersonBean person = new BoundPersonBean();
        person.addPropertyChangeListener(evt -> {
            System.out.println("Name changed from " + evt.getOldValue() + " to " + evt.getNewValue());
        });

        person.setName("Alice");
        person.setName("Bob");
    }
}
```

*Result:* The example demonstrates a Java Bean with a bound property, notifying listeners of changes.

---

**Q3. [Unit IV | Topic: Servlet Life Cycle | Type: Applied | Difficulty: Intermediate]**  
**Question:** Write a servlet that demonstrates the servlet life cycle methods.  

*Concept from scratch:* A servlet goes through several life cycle stages: initialization (`init`), request handling (`service`), and destruction (`destroy`). These methods can be overridden to define specific behavior.

*Example:*

```java
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;

public class LifeCycleServlet extends HttpServlet {
    public void init() throws ServletException {
        // Initialization code
        System.out.println("Servlet Initialized");
    }

    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<h1>Servlet Life Cycle Example</h1>");
        out.println("<p>Handling a request.</p>");
    }

    public void destroy() {
        // Cleanup code
        System.out.println("Servlet Destroyed");
    }
}
```

*Result:* The servlet demonstrates its life cycle by printing messages during initialization, handling requests, and destruction.

---

### Section C: Advanced Theory & Numericals

**Q1. [Unit IV | Topic: Java Beans API | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the Java Beans API and its significance in Java development.  

*Concept from scratch:* The Java Beans API provides a way to create reusable software components that can be manipulated in visual development environments. It defines standards for creating, accessing, and managing Java Beans, facilitating their integration into applications and frameworks.

*Result:* The Java Beans API significantly enhances component-based development in Java.

---

**Q2. [Unit IV | Topic: Session and Entity Beans | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the differences between session beans and entity beans in Java EE.  

*Concept from scratch:* 
- **Session Beans:** These are used to represent business logic and can be stateless or stateful. They handle client requests and do not persist data beyond the session.
- **Entity Beans:** These are used to represent persistent data and are associated with a specific database table. They maintain their state across transactions and can be used to manipulate database records.

*Result:* Session beans handle business logic, while entity beans manage persistent data in Java EE applications.

---

**Q3. [Unit IV | Topic: Servlet API | Type: Numerical | Difficulty: Advanced]**  
**Question:** Create a web application using servlets that handles form data submission and displays the result.  

*Concept from scratch:* Servlets can process form data submitted via HTTP POST or GET methods. You need to retrieve the data from the request object, process it, and generate a response.

*Example:*

```java
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;

public class FormHandlingServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name = request.getParameter("name");
        String email = request.getParameter("email");

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<h1>Form Submission Result</h1>");
        out.println("<p>Name: " + name + "</p>");
        out.println("<p>Email: " + email + "</p>");
    }
}
```

*Result:* The servlet processes form data and displays the submitted information.

--- 

This completes the detailed step-wise solutions for the BCS-203 Object Oriented Programming question bank, covering all units and types of questions as requested.