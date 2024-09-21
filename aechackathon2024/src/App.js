import './App.css';
import {APIProvider, Map, MapCameraChangedEvent} from '@vis.gl/react-google-maps';
import  ZipToGeo  from './utilities/ziptogeo'
import { useState, useEffect } from 'react';
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
  const [price, setPrice] = useState('')
  const [zip, setZipCode] = useState('')
  const [propertyType, setPropertyType] = useState('')
  const [latitude, setLatitude] = useState(34.052235)
  const [longitude, setLongitude] = useState(-118.243683)
  
  const submit = (e) =>{
    e.preventDefault();

    let lat, long;
    ({lat, long} =  ZipToGeo(zip));
    setLatitude(lat)
    setLongitude(long)
  }


  return (<div className="App">
      <h1 id ="title">Find Your Apartment</h1>
      <Container >
        <Row>
          <Col></Col>
          <Col xl={3}>
            <Form className="p-4" id="initial-form" onSubmit={submit} >
              <FormGroup>
                <Label htmlFor="price">Price</Label>
                <Input type="number" name="price" id="price" placeholder="Enter your price" value={price} onChange={(e) => setPrice(e.target.value)} />
              </FormGroup>
              <FormGroup>
                <Label htmlFor="zip">Zip Code</Label>
                <Input type="number" name="zip" id="zip" placeholder="What is your zip code?" value={zip} onChange={(e) => setZipCode(e.target.value)}  />
              </FormGroup>
              <FormGroup>
                <Label htmlFor="propertyType">Property Type</Label><br />
                <Input type="select" name="propertyType" id="propertyType" value={propertyType} onChange={(e) => setPropertyType(e.target.value)}  >
                  <option value="2">Apartment</option>
                  <option value="3">House</option>
                </Input>
              </FormGroup>
              <Button color="primary">Find Your Apartment!</Button>
            </Form>
          </Col>
          <Col></Col>
        </Row>
      </Container>
      <div id="googlemaps">
      <APIProvider apiKey={'AIzaSyBR4OUYOMC4iSFYayAdkfgjfc_itpVDGfA'} onLoad={() => console.log('Maps API has loaded.')}>
        <Map
            defaultZoom={13}
            center={ { lat: latitude, lng: longitude } }
            onCameraChanged={ (ev: MapCameraChangedEvent) =>
            console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)
            }>
        </Map>
        </APIProvider>
      </div>
  </div>
  );
}

export default App;
