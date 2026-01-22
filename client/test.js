import axios from 'axios';

const base = 'http://localhost:8000';

async function run() {
  try {
    console.log('health:', (await axios.get(`${base}/health`)).data);

    const payload = { follower_id: 'alice', following_id: 'bob' };

    console.log('follow:', (await axios.post(`${base}/follow`, payload)).data);
    console.log('followers of bob:', (await axios.get(`${base}/followers/bob`)).data);
    console.log('following of alice:', (await axios.get(`${base}/following/alice`)).data);

    console.log('unfollow:', (await axios.post(`${base}/unfollow`, payload)).data);
    console.log('followers of bob after:', (await axios.get(`${base}/followers/bob`)).data);
  } catch (e) {
    if (e.response) console.error('error:', e.response.status, e.response.data);
    else console.error(e.message);
    process.exit(1);
  }
}

run();
