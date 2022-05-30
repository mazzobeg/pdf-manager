
<div  align="center">

<h1> <img  src="https://github.com/mazzobeg/PDFManager/blob/WIP/contents/pdf.jpg"  width="80px"><br/>PDFManager</h1>

</div>

  
  

### Description

Little python script which automatize different tasks about your pdf to keep them clean and organized.

 
### Features

Current feature :
- Automatic rename pdf file / folder who contain pdfs with metadatas information.

Future :
- Creation of shelf sumary file to manage reading.
- Improving renamer to use keyword if title not provided by metadatas.
- Intelligent classification.
- More ... 
  
### How to Setup:

- git clone 
- cd [path_to_package]
- pip install
- touch .env
	- copy paste in the file : SHELFPATH=[path_to_your_shelf]
- add an alias to your terminal :
	- ~/.zshrc
	- copy paste : alias _pdf='python [path_to_package]/cli.py'

### Test your setup:
- open a new terminal 
- _pdf -h

### Example

![terminal](/contents/terminal.png?raw=true)

![shelf](/contents/result.png?raw=true)

### References

| Flag | Option | Description |
| ----------- | ----------- | ----------- |
| -d | `--dirpath [path:str]`| the folder path containing the pdfs to rename |
|-f| `--filepath [path:str]` | the path of pdf to rename |
|-h| `--help [path:str]` |help |


  

### Tech Used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

  




  

 
