// Masala 1: Foydalanuvchidan son kiritishini sorang, agar son 0 ga teng bolganda sikl toxyasin
while(true){
    let son = Number(prompt("son kiriting:"))
    if (son === 0){
        break
    }
}
// Masala 2: switch-case yordamida kalkulyator yasash.
let son1 = Number(prompt("birinchi sonni kiriting: "))
let son2 = Number(prompt("ikkinchi sonni kiriting: "))
let amal = Number(prompt("1,2,3,4 kiriting: 1-qoshish , 2-ayirish, 3-kopaytirish, 4-bolish"))
switch(amal){
    case 1:
        console.log( son1 + son2);
        break
    case 2:
        console.log( son1 - son2);
        break
    case 3:
        console.log( son1 * son2);
        break
    case 4:
        console.log( son1 / son2);
        break
    default:
        console.log( "bunday ishora yoq");
}
//Masala 3:
i = 1
while(i <= 100){
    if (i % 3 == 0){
        i++
        continue
    }else{
        console.log(i)
        i++
    }
}