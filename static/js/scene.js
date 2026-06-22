import * as THREE from 'three';

const canvas = document.getElementById('scene-canvas');
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(window.innerWidth, window.innerHeight);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 200, 0);
camera.up.set(0, 0, 1);
camera.lookAt(0, 0, 0);

const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

const objects = [];

const radius = 1;
const widthSegments = 6;
const heightSegments = 6;
const sphereGeometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);

const sunMaterial = new THREE.MeshPhongMaterial({ emissive: 0xffff00 });
const sunMesh = new THREE.Mesh(sphereGeometry, sunMaterial);
sunMesh.scale.set(10, 10, 10);
scene.add(sunMesh);
objects.push(sunMesh);

{
    const color = 0xffffff;
    const intensity = 500;
    const light = new THREE.PointLight(color, intensity);
    scene.add(light);
}

const earthMaterial = new THREE.MeshPhongMaterial({ color: 0x2233FF, emissive: 0x112244 });
const earthMesh = new THREE.Mesh(sphereGeometry, earthMaterial);
earthMesh.position.x = 10;
sunMesh.add(earthMesh);
objects.push(earthMesh);

function animate(time) {
    requestAnimationFrame(animate);
    objects.forEach((obj) => {
        obj.rotation.y = time / 1000;
    });
    renderer.render(scene, camera);
}
animate();
