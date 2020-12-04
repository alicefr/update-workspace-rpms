# Update rpm in WORKSPACE file for cdi
Build the container image:
```bash
docker build --tag fetch-workspace . 
```
Run the script in the dir of your input WORKSPACE
```bash
docker run -ti --security-opt label=disable -v $(pwd):/out fetch-workspace python3 fetch-repo-workspace.py -i WORKSPACE -o output
```


