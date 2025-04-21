import { CardMedia } from "@mui/material";

export default function PostMedia({
  mediaUrl = null,
  isVideo = false,
  isPhoto = true,
} = {}) {
  if (!mediaUrl) return null;

  if (isVideo) {
    return (
      <CardMedia
        component="video"
        src={mediaUrl}
        controls
        autoPlay
        muted
        loop
        playsInline
      />
    );
  } else if (isPhoto) {
    return <CardMedia component="img" image={mediaUrl} />;
  } else {
    return <></>;
  }
}
