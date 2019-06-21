function hello(name){
	return 'Hello ' + name;
}

console.log(hello());

function toCelcius(fahrenheit){
	return (5/9) * (fahrenheit - 32);
}

function print_arguments(){
	for(let arg of arguments){
		console.log(arg);
	}
}
// default parameter
function hello(name){
	if(name === undefined) name = 'stranger'
	console.log('Hello ' + name);
}

// new way
function hello(name='stranger'){
	console.log(`Hello ${name}`)
}

// a shorter way
let hello_arrow = (name='stranger') => 'Hello ' + name

// Objects (like dictionaries in python. this is equivalent to self)
let bite = {'number': 1, 'title': 'sum of numbers', 'points': 2}
bite.str = function(){console.log(`Bite : ${this.number} - ${this.title} - points ${this.points}`)}