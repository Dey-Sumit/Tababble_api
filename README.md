# Tababble API using python

Extract all the focusable elements (web element that can be selected using tab) from a web page maintaining the order using python and selenium



### Prerequisites

python packages you need to install :

```
selenium (version:3 or higher)
```
Browser Driver (eg: Chrome web driver)


## Set up

1. Download the tab.py file or clone the repo
2. change the webdriver location if needed
```
driver = webdriver.Chrome(executable_path=r"C:\Users\Sumax\Desktop\Selenium\chromedriver.exe")
``` 
3. That's all , run the tab.py file

## Running the test
When you run the file,
1. This program first asks for the URL(user input) for which you want to extract the elements
2. Then it checks the validation of the URL using regex
3. If it passed , it extracts all the focusable elements and store it as an object with details in a global list of objects
4. You can then create an excel sheet using the array of objects


## Built With

* [Selenium](https://pypi.org/project/selenium/) - The selenium package is used to automate web browser interaction from Python.


## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.

## Author

* **Sumit Dey** -  [Dey-Sumit](https://github.com/Dey-Sumit/)



## License

This project is free to use,
feel free to fork the project
