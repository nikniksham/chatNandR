import React, {useState, useEffect} from 'react';
import Counter from "./components/Counter";
import ClassCounter from "./components/ClassCounter"
import TestLoad from "./components/TestLoad"
import test from "./actions/test"

function App() {
    const [data, setData] = useState([{}])

    /*useEffect(() => {
        fetch("/members").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])*/
  return (
    <div className="App">
        <Counter/>
        <button onClick={() => test("рот твой шатал")}>Рот твой шатал</button>
        /*{(typeof data.members === 'undefined') ? (
            <p>Loading... plz WAIT!</p>
        ) : (
            data.members.map((member, i) => (
                <p key={i}>{member}</p>
            ))
        )}*/
    </div>
  );
}

export default App;
