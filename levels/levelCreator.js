const fs = require("fs")

const readLineSync = require("readline-sync")

let dimension = readLineSync.question("Velkost pola? ")
while(!/^[1-9]$/.test(dimension)){
    console.log("rozmer musi byt od 1-9")
    dimension = readLineSync.question("velkost pola?" )
}

let resJson = {
    dimension,
    tiles:[]
}

for(let row = 0; row < dimension; row++){
    for(let col = 0; col < dimension; col++){
        console.clear()
        console.log(`Vytvarate bunku row = ${row} col = ${col}`)
        console.log("Zadaj na ktorych stranach ma byt ohranicenie (hore - u, prava - r, dole - d, lava - l)")
        console.log("Napriklad chcem ohranicenie hore, napravo a nalavo tak zadam: url")
        let border = readLineSync.question(" ")
        while(!border.match(/[urdl]/g)){
            console.log("zadali ste nespravne ohranicenie, povolene znaky su iba (u,r,d,l)")
            border = readLineSync.question(" ")
        }
        let label = readLineSync.question("Zadajte label (ak label nema byt v danej bunke stlacte enter) ")
        let newTile = {row, col, border, label}
        resJson.tiles.push(newTile)
    }
}

let data = JSON.stringify(resJson)
let levelNum = readLineSync.question("Zadajte cislo levelu: ")
fs.writeFileSync(`level${levelNum}.json`, data, err => console.log("Chyba pri zapise", err))