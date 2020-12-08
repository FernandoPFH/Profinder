function SearchForProjects () {
    sessionStorage.setItem("searchbarvalue",document.getElementById("SearchBar").value);
    
    window.location.href = "/projects/";
}