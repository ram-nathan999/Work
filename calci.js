function appendToScreen(value)
{
    document.getElementById('screen').value += value;
}

function clearScreen()
{
    document.getElementById('screen').value = '';
}

function calculate()
{
    let screenValue = document.getElementById('screen').value;
    let result = eval(screenValue); 
    document.getElementById('screen').value = result;
}