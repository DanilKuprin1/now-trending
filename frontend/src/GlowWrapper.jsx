import { Box } from "@mui/material";
import { useEffect, useState } from "react";

const GlowWrapper = ({ children, objectToTrack }) => {
  const [isGlowing, setIsGlowing] = useState(true);

  useEffect(() => {
    setIsGlowing(true);
    const timeout = setTimeout(() => {
      setIsGlowing(false);
    }, 2000);
    return () => clearTimeout(timeout);
  }, [objectToTrack]);

  return (
    <Box
      sx={{
        position: "relative",
        overflow: "hidden",
        borderRadius: 2,
        transition:
          "box-shadow 350ms cubic-bezier(.4,0,.2,1), transform 350ms cubic-bezier(.4,0,.2,1)",

        "&::before": {
          content: '""',
          position: "absolute",
          inset: -2,
          zIndex: -1,
          borderRadius: "inherit",

          background:
            "linear-gradient(45deg,#00eaff,#8e00ff,#ff00c8,#ff8a00,#00eaff)",
          backgroundSize: "400% 400%",
          filter: "blur(14px)",
          opacity: isGlowing ? 0.9 : 0,
          transition: "opacity 300ms ease-in-out",
          animation: isGlowing ? "glowShift 4s linear infinite" : "none",
        },
        boxShadow: isGlowing
          ? `0 0 3px rgba(255,255,255,.6),
         0 0 8px rgba(0,234,255,.6),
         0 0 16px rgba(142,0,255,.4)`
          : "0 1px 3px rgba(0,0,0,.4)",

        transform: isGlowing ? "translateY(-2px) scale(1.02)" : "none",
        willChange: "transform, box-shadow",
      }}
    >
      {children}
    </Box>
  );
};

export default GlowWrapper;
