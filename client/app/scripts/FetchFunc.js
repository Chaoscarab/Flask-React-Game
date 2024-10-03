const fetchFunc = async (route, method, object = {},) => {
    //port and local host
    let url = "http://127.0.0.1:5000" + route
    let FetchObj = {
        method: method,
        headers: {
          'Accept': 'application/json',
          "Content-Type": "application/json"
        }}

    if (method === "POST"){
        FetchObj.body = JSON.stringify(object)
    }
    try{
        const rawResponse = await fetch(url,FetchObj);
        let passback = await rawResponse.json();
        return passback
    }catch (e) {
        console.log(e)
        throw Error
    }
}

export default fetchFunc