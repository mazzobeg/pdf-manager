
<div  align="center">

<h1> 📄 <br/>PDFManager</h1>

</div>

### Description & Features 📚

Small python cli that automates different tasks on your pdfs to keep them clean and organized.

Current feature:
- Automatically rename files/folders containing PDF files with metadata information.

Coming :
- Creation of a librarian summary file to manage reading.
- Improved renaming with the use of keywords if the title is not provided by the metadata.
- Smart ranking.
- After ...
  
### How to Setup (~2min) ⚙️

```
git clone https://github.com/mazzobeg/PDFManager
cd [path_to_package]
pip install
touch .env
echo "SHELFPATH=[path_to_your_shelf]" > .env
```
### Run it! ⏯
#### Boring way
```
python [path_to_package]/cli.py -h
```
#### Efficient way
Add an alias to your shell. For example if you use zsh :
```
echo 'alias _pdf='python [path_to_package]/cli.py' >> ~/.zshrc
```
Open a new terminal and run :
```
_pdf -h
```
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
