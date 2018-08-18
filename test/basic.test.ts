import * as mocha from 'mocha';
import * as chai from 'chai';
import chaiHttp = require('chai-http');

import app from '../src/App';

chai.use(chaiHttp);
const expect = chai.expect;

describe('baseRoute', () => {
  it('should be json', async () => {
    let res = await chai.request(app).get('/');
    expect(res.type).to.eql('application/json');
  });

  it('should have a message prop', async () => {
    let res = await chai.request(app).get('/');
    expect(res.body.message).to.eql('Hello World!');
  });
});