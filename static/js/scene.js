import * as THREE from 'three';

const canvas = document.getElementById('scene-canvas');
const renderer = new THREE.WebGLRenderer({ canvas });

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 1000);
camera.position.set(0, 200, 0);
camera.up.set(0, 0, 1);
camera.lookAt(0, 0, 0);

const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

const objects = [];

// Creates Object Dimensions and mesh
const ObjectCreation = {
    sphere: () => new THREE.Mesh(
        new THREE.SphereGeometry(5,16,16),
        new THREE.MeshPhongMaterial({color: 0x44AA88})
    ),
    cube: () => new THREE.Mesh(
        new THREE.BoxGeometry(8,8,8),
        new THREE.MeshPhongMaterial({color:0xAA4444})
    ),
};

// Handles adding objects to the canvas
function addObject(type, position = null) {
    const creation = ObjectCreation[type.toLowerCase()];
    if(!creation) return;
    const mesh = creation();
    mesh.position.copy(position ?? new THREE.Vector3(
        (Math.random() - 0.5) * 40, 0, (Math.random() - 0.5) * 40
    ));
    scene.add(mesh);
    objects.push(mesh);
}

// detects when and object is dragged and dropped onto a screen.
document.querySelectorAll('.sidenav-object-btn').forEach(btn => {
    btn.addEventListener('dragstart', e => {
        e.dataTransfer.setData('objectType', btn.dataset.type); // Places an object where you drag and drop it
    });
});

const raycaster = new THREE.Raycaster();
const groundPlane = new THREE.Plane(new THREE.Vector3(0,1,0), 0);

canvas.addEventListener('dragover', e => e.preventDefault());

canvas.addEventListener('drop', e => {
    e.preventDefault();
    const type = e.dataTransfer.getData('objectType');

    const rect = canvas.getBoundingClientRect();
    const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
    );

    raycaster.setFromCamera(mouse, camera);
    const dropPos = new THREE.Vector3();
    raycaster.ray.intersectPlane(groundPlane, dropPos);

    addObject(type, dropPos);
});

function handleResize() {
    const rect = canvas.getBoundingClientRect();
    const w = window.innerWidth - rect.left;
    const h = window.innerHeight - rect.top;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
}

window.addEventListener('resize', handleResize);
handleResize();

function animate(time) {
    requestAnimationFrame(animate);
    objects.forEach((obj) => {
        obj.rotation.y = time / 1000;
        obj.rotation.x = time / 2000;
    });
    renderer.render(scene, camera);
}
animate();
