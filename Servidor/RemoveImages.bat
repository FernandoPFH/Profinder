for /f "tokens=3" %%i in ('docker images') do (
    docker rmi -f %%i
)