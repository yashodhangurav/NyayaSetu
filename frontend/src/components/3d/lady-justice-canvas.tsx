"use client";

import React, {
  Suspense,
  useRef,
  useEffect,
  useState,
  useCallback,
  Component,
  type ErrorInfo,
  type ReactNode,
} from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { useGLTF, ContactShadows } from "@react-three/drei";
import * as THREE from "three";

const MODEL_PATH = "/models/lady-justice/model.glb";

// Preload the GLB model into browser cache for instant rendering
if (typeof window !== "undefined") {
  useGLTF.preload(MODEL_PATH);
}

// Error Boundary to gracefully handle WebGL or GPU context errors
interface ErrorBoundaryProps {
  children: ReactNode;
  fallback: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

class WebGLErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.warn("WebGL Lady Justice Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// The 3D Lady Justice Sculpture Component inside R3F Canvas
interface LadyJusticeModelProps {
  rotationOffset: { x: number; y: number };
  isInteracting: boolean;
  onLoaded?: () => void;
}

function LadyJusticeModel({
  rotationOffset,
  isInteracting,
  onLoaded,
}: LadyJusticeModelProps) {
  const groupRef = useRef<THREE.Group>(null);
  const { scene } = useGLTF(MODEL_PATH);
  const idlePhase = useRef(0);

  // Front-facing angle turned towards viewer
  const BASE_ROTATION_Y = -0.50;

  // Enhance bronze materials, configure shadows, and register cleanup
  useEffect(() => {
    if (!scene) return;

    scene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        mesh.castShadow = true;
        mesh.receiveShadow = true;

        if (
          mesh.material &&
          (mesh.material as THREE.MeshStandardMaterial).isMeshStandardMaterial
        ) {
          const mat = mesh.material as THREE.MeshStandardMaterial;
          mat.envMapIntensity = 1.35;
          mat.roughness = 0.52;
          mat.metalness = 0.82;
          mat.needsUpdate = true;
        }
      }
    });

    if (onLoaded) {
      onLoaded();
    }

    // Comprehensive WebGL cleanup on unmount to prevent memory leaks
    return () => {
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          if (mesh.geometry) {
            mesh.geometry.dispose();
          }
          if (mesh.material) {
            const materials = Array.isArray(mesh.material)
              ? mesh.material
              : [mesh.material];
            materials.forEach((m) => {
              Object.keys(m).forEach((key) => {
                const prop = (m as unknown as Record<string, unknown>)[key];
                if (prop && typeof (prop as { dispose?: () => void }).dispose === "function") {
                  (prop as { dispose: () => void }).dispose();
                }
              });
              m.dispose();
            });
          }
        }
      });
    };
  }, [scene, onLoaded]);


  // Smooth continuous rotation & responsive interactive tilt
  useFrame((_, delta) => {
    if (!groupRef.current) return;

    // Guard against large delta jumps when switching browser tabs
    const dt = Math.min(delta, 0.1);

    if (!isInteracting) {
      // Subtle majestic living breathing motion: +- 3.5 degrees keeping face strictly front-facing
      idlePhase.current += dt * 0.80;
      const idleY = BASE_ROTATION_Y + Math.sin(idlePhase.current) * 0.1;
      const idleX = Math.cos(idlePhase.current * 0.7) * 0.025;

      groupRef.current.rotation.y = THREE.MathUtils.lerp(
        groupRef.current.rotation.y,
        idleY,
        dt * 5.0
      );
      groupRef.current.rotation.x = THREE.MathUtils.lerp(
        groupRef.current.rotation.x,
        idleX,
        dt * 5.0
      );
    } else {
      // Smoothly track user pointer / drag interaction
      const targetY = BASE_ROTATION_Y + rotationOffset.x;
      const targetX = rotationOffset.y;

      groupRef.current.rotation.y = THREE.MathUtils.lerp(
        groupRef.current.rotation.y,
        targetY,
        dt * 6.5
      );
      groupRef.current.rotation.x = THREE.MathUtils.lerp(
        groupRef.current.rotation.x,
        targetX,
        dt * 6.5
      );
    }
  });

  return (
    // Scaled to 0.94 and positioned at x = -0.05 to balance with the concentric seal ring
    // and provide clean breathing margins from the practice chips on the right
    <group ref={groupRef} position={[-0.05, -0.02, 0]} scale={0.94}>
      <primitive object={scene} />

      {/* Realistic contact grounding shadow directly beneath circular pedestal */}
      <ContactShadows
        position={[0, -1.01, 0]}
        opacity={0.44}
        scale={2.2}
        blur={2.5}
        far={1.6}
        color="#2a1c12"
      />
    </group>
  );
}

// Studio Lighting rig tailored for antique bronze reflection and sculpture depth
function SculptureStudioLighting() {
  return (
    <>
      {/* Warm ambient base */}
      <ambientLight intensity={0.92} color="#fff6eb" />

      {/* Primary Key Light - Warm sun/studio spotlight creating crisp highlights */}
      <directionalLight
        position={[3.0, 4.2, 3.5]}
        intensity={2.6}
        color="#fff4e0"
        castShadow
        shadow-mapSize={[1024, 1024]}
        shadow-bias={-0.0001}
        shadow-camera-near={0.5}
        shadow-camera-far={10}
        shadow-camera-left={-1.5}
        shadow-camera-right={1.5}
        shadow-camera-top={2}
        shadow-camera-bottom={-2}
      />

      {/* Secondary Fill Light - Soft cool fill softening deep drapery crevices */}
      <directionalLight
        position={[-3.5, 2.2, 2.8]}
        intensity={1.3}
        color="#dbe5f0"
      />

      {/* Golden Rim / Kicker Light - Accents hair curls, blindfold, and sword silhouette */}
      <directionalLight
        position={[0, 4.5, -4.0]}
        intensity={3.4}
        color="#ffd699"
      />

      {/* Golden Scale Accent Light - Direct specular highlight on balance beam & pans */}
      <pointLight
        position={[1.3, 2.0, 1.4]}
        intensity={1.8}
        distance={6}
        color="#ffe2a3"
      />

      {/* Steel/Sword Accent Light - Sharp glint down the ceremonial blade */}
      <pointLight
        position={[-1.2, -0.3, 1.2]}
        intensity={1.4}
        distance={4.5}
        color="#e3ecf5"
      />

      {/* Warm parchment bounce from ground plane */}
      <directionalLight
        position={[0, -3.2, 1.2]}
        intensity={0.65}
        color="#f4efe6"
      />
    </>
  );
}

// Minimal bronze loading spinner component with smooth fade
export function LadyJusticeLoader({ isExiting = false }: { isExiting?: boolean }) {
  return (
    <div
      className={`absolute inset-0 flex flex-col items-center justify-center pointer-events-none z-10 transition-opacity duration-700 ease-out ${isExiting ? "opacity-0" : "opacity-100"
        }`}
      aria-label="Loading 3D Statue"
    >
      <div className="relative w-11 h-11 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border border-[#9a6a35]/25 animate-ping" />
        <div className="w-7 h-7 rounded-full border-2 border-[#9a6a35]/20 border-t-[#9a6a35] animate-spin" />
      </div>
      <span className="mt-3 text-[10px] font-sans font-medium uppercase tracking-[0.22em] text-[#9a6a35]/80 select-none">
        Loading 3D Statue
      </span>
    </div>
  );
}

// Fallback component if WebGL is unavailable
function LadyJusticeFallback() {
  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="w-4/5 h-4/5 rounded-full border border-[#9a6a35]/20 flex items-center justify-center text-[#9a6a35]/60 text-xs">
        Lady Justice 3D
      </div>
    </div>
  );
}

// Main Exported Canvas Component with IntersectionObserver & Event Handlers
export function LadyJusticeCanvas() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(true);
  const [rotationOffset, setRotationOffset] = useState({ x: 0, y: 0 });
  const [isInteracting, setIsInteracting] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Performance Optimization: Pause rendering when scrolled out of view
  useEffect(() => {
    const el = containerRef.current;
    if (!el || typeof IntersectionObserver === "undefined") return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsInView(entry.isIntersecting);
      },
      { threshold: 0.05 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  // Drag tracking refs
  const isDraggingRef = useRef(false);
  const lastPointerRef = useRef({ x: 0, y: 0 });
  const accumulatedRotationRef = useRef({ x: 0, y: 0 });

  const handlePointerDown = useCallback((e: React.PointerEvent<HTMLDivElement>) => {
    isDraggingRef.current = true;
    setIsInteracting(true);
    lastPointerRef.current = { x: e.clientX, y: e.clientY };
    (e.target as HTMLElement).setPointerCapture?.(e.pointerId);
  }, []);

  const handlePointerMove = useCallback((e: React.PointerEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;

    if (isDraggingRef.current) {
      // Active drag / swipe rotation
      const deltaX = e.clientX - lastPointerRef.current.x;
      const deltaY = e.clientY - lastPointerRef.current.y;
      lastPointerRef.current = { x: e.clientX, y: e.clientY };

      accumulatedRotationRef.current = {
        x: Math.max(-0.8, Math.min(0.8, accumulatedRotationRef.current.x + deltaX * 0.007)),
        y: Math.max(-0.25, Math.min(0.25, accumulatedRotationRef.current.y - deltaY * 0.004)),
      };
      setRotationOffset({ ...accumulatedRotationRef.current });
    } else {
      // Gentle hover parallax tracking
      const rect = containerRef.current.getBoundingClientRect();
      const nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const ny = ((e.clientY - rect.top) / rect.height) * 2 - 1;
      setRotationOffset({
        x: Math.max(-1, Math.min(1, nx)) * 0.45,
        y: Math.max(-1, Math.min(1, ny)) * -0.12,
      });
    }
  }, []);

  const handlePointerUp = useCallback((e: React.PointerEvent<HTMLDivElement>) => {
    isDraggingRef.current = false;
    setIsInteracting(false);
    accumulatedRotationRef.current = { x: 0, y: 0 };
    setRotationOffset({ x: 0, y: 0 });
    try {
      (e.target as HTMLElement).releasePointerCapture?.(e.pointerId);
    } catch {
      // Ignore if pointer capture was already released
    }
  }, []);

  const handlePointerEnter = useCallback(() => {
    if (!isDraggingRef.current) {
      setIsInteracting(true);
    }
  }, []);

  const handlePointerLeave = useCallback(() => {
    if (!isDraggingRef.current) {
      setIsInteracting(false);
      accumulatedRotationRef.current = { x: 0, y: 0 };
      setRotationOffset({ x: 0, y: 0 });
    }
  }, []);

  return (
    <WebGLErrorBoundary fallback={<LadyJusticeFallback />}>
      <div
        ref={containerRef}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerCancel={handlePointerUp}
        onPointerEnter={handlePointerEnter}
        onPointerLeave={handlePointerLeave}
        className="relative w-full h-full cursor-grab active:cursor-grabbing select-none"
        style={{ touchAction: "pan-y" }}
        title="Interactive 3D Lady Justice - Move cursor or drag to inspect"
      >
        {/* Loading Spinner with smooth fade out when loaded */}
        <LadyJusticeLoader isExiting={isLoaded} />

        <Canvas
          shadows
          frameloop={isInView ? "always" : "never"}
          gl={{
            alpha: true,
            antialias: true,
            powerPreference: "high-performance",
            toneMapping: THREE.ACESFilmicToneMapping,
            toneMappingExposure: 1.18,
          }}
          camera={{
            position: [0, -0.02, 3.65],
            fov: 36,
            near: 0.1,
            far: 20,
          }}
          dpr={[1, 2]}
          style={{
            width: "100%",
            height: "100%",
            background: "transparent",
            pointerEvents: "auto",
          }}
        >
          <SculptureStudioLighting />

          <Suspense fallback={null}>
            <LadyJusticeModel
              rotationOffset={rotationOffset}
              isInteracting={isInteracting}
              onLoaded={() => setIsLoaded(true)}
            />
          </Suspense>
        </Canvas>
      </div>
    </WebGLErrorBoundary>
  );
}
