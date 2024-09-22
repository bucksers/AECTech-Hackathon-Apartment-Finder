import './App.css';
import {APIProvider, Map, MapCameraChangedEvent, AdvancedMarker, Pin } from '@vis.gl/react-google-maps';
import  ZipToGeo  from './utilities/ziptogeo'
import { useState } from 'react';
import {
  Button,
  Form,
  FormGroup,
  Label,
  Container,
  Row,
  Col,
  Input
} from 'reactstrap'

function App() {
  const [ price, setPrice ] = useState('')
  const [ zip, setZipCode ] = useState('90017')
  const [ propertyType, setPropertyType ] = useState('')
  const [ latitude, setLatitude ] = useState(34.052913)
  const [ longitude, setLongitude ] = useState(-118.264340)

  const [  posits, setPosits  ] = useState([
    {key: '1', location: { lat: 34.039378, lng: -118.266300  }},
    {key: '2', location: { lat: 34.028331, lng: -118.354338  }},
    {key: '3', location: { lat: 34.028887, lng: -118.317183  }},
    {key: '4', location: { lat: 34.049841, lng: -118.338460  }}
  ])
  
  const submit = async (e) =>{
    e.preventDefault();

    let lat, lng;
    ({lat, lng} =  ZipToGeo(zip));
    setLatitude(lat)
    setLongitude(lng)

    const response = await fetch('http://127.0.0.1:5000/rank-areas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        zip: zip, 
        price: price, 
        propertyType: propertyType
      })
    });

    const data = await response.json();
    if (data.status === 'success') {
      const rankedAreas = data.data;

      // Update the positions based on the API response
      setPosits([
        { key: '1', location: ZipToGeo((zip - 2).toString()) },
        { key: '2', location: ZipToGeo((zip - 1).toString()) },
        { key: '3', location: ZipToGeo((zip + 1).toString()) },
        { key: '4', location: ZipToGeo((zip + 2).toString()) }
      ]);
      
      console.log('Ranked Areas:', rankedAreas);
    } else {
      console.error('There is Error:', data.message);
    }

  };


  return (<div className="App">
      <h1 id ="title">Find Your Zip Code
      </h1>
      <Container >
        <Row className="justify-content-center">
            <Form className="p-4" id="initial-form" onSubmit={submit} >
              <FormGroup row>
                <Label htmlFor="price" check>Price</Label>
                <Col sm={10}>
                  <Input type="number" name="price" id="price" placeholder="Enter your price" value={price} onChange={(e) => setPrice(e.target.value)} />
                </Col>
              </FormGroup>
              <FormGroup row>
                <Label htmlFor="zip">Zip Code</Label>
                <Col sm={10}>
                  <Input type="number" name="zip" id="zip" placeholder="What is your zip code?" value={zip} onChange={(e) => setZipCode(e.target.value)}  />
                </Col>
              </FormGroup>
              <FormGroup row>
                <Label htmlFor="propertyType">Property Type</Label><br />
                <Col sm={10}>
                <Input type="select" name="propertyType" id="propertyType" value={propertyType} onChange={(e) => setPropertyType(e.target.value)}  >
                  <option value="2">Apartment</option>
                  <option value="3">House</option>
                </Input>
                </Col>
              </FormGroup>
              <Button color="primary">Find Your Zip Code!</Button>
            </Form>
        </Row>
      </Container>
      <div id="googlemaps">
      <APIProvider apiKey={'AIzaSyBR4OUYOMC4iSFYayAdkfgjfc_itpVDGfA'} onLoad={() => console.log('Maps API has loaded.')}>
        <Map
            defaultZoom={10}
            center={ { lat: latitude, lng: longitude } }
    mapId='DEMO_MAP_ID'
            onCameraChanged={ (ev: MapCameraChangedEvent) =>
            console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)
            }>
        </Map>
          <AdvancedMarker
            position={{ lat: latitude, lng: longitude }}>
          </AdvancedMarker>
          {posits.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ posit.location }>
              <Pin background={'#FBBC04'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
        </APIProvider>
      </div>
  </div>
  );
}

export default App;
