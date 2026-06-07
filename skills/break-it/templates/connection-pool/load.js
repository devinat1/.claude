import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 100 }, // ramp to 100 virtual users
    { duration: '20s', target: 100 }, // hold at 100
    { duration: '5s', target: 0 },    // ramp down
  ],
  thresholds: {
    // The wall. Naive breaches p(99); patched stays under it. k6 exits
    // non-zero when a threshold fails, so these ARE the pass/fail assertion.
    http_req_duration: ['p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('http://localhost:8081/');
  check(res, { 'status 200': (r) => r.status === 200 });
}
