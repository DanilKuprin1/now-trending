import {
  Card,
  CardHeader,
  CardContent,
  CardActions,
  Avatar,
  IconButton,
  Typography,
  Box,
  Grid,
} from "@mui/material";
import FavoriteIcon from "@mui/icons-material/Favorite";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import RepeatIcon from "@mui/icons-material/Repeat";
import VisibilityIcon from "@mui/icons-material/Visibility";
import PostMedia from "./PostMedia";

export default function Post({
  userName,
  userSceenName,
  avatarUrl,
  createdAt,
  text,
  favorites,
  replies,
  retweets,
  views,
  media,
}) {
  let mediaUrl = null;
  if (media) {
    mediaUrl = media[0];
  }

  if (createdAt) {
    const utcTime = "Sat Apr 12 14:22:29 +0000 2025";
    const localTime = new Date(utcTime);
    const options = {
      weekday: "short",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    };
    const formatted = localTime.toLocaleString("en-US", options);
    createdAt = formatted.replace(",", "").replace(/\s\d{4}$/, "");
  }

  return (
    <Card elevation={0}>
      <CardHeader
        avatar={<Avatar src={avatarUrl} />}
        title={
          <Typography fontWeight="bold">
            {userName}{" "}
            <Typography
              component="span"
              color="text.secondary"
              fontWeight="normal"
            >
              {userSceenName}
            </Typography>
          </Typography>
        }
        subheader={createdAt}
      />
      <CardContent>
        <Typography variant="body1">{text}</Typography>
      </CardContent>
      <Box borderRadius={1} overflow={"hidden"} marginInline={1}>
        <Grid
          container
          spacing={0}
          sx={{
            maxWidth: "100%",
            maxBlockSize: "100%",
            display: "flex",
            flexWrap: "wrap",
          }}
          alignContent={"center"}
          justifyContent={"center"}
        >
          {media
            ? media.map((mediaItem, index) => {
                const isLast = index === media.length - 1;
                const isOdd = media.length % 2 !== 0;
                const shouldSpanFull = isOdd && isLast;

                return (
                  <Grid
                    key={mediaItem["source"]}
                    style={{
                      flexBasis: shouldSpanFull ? "100%" : "50%",
                      maxWidth: shouldSpanFull ? "100%" : "50%",
                    }}
                    alignContent={"center"}
                  >
                    <Box>
                      <PostMedia
                        mediaUrl={mediaItem["source"]}
                        isVideo={mediaItem["content_type"] === "video"}
                        isPhoto={mediaItem["content_type"] === "photo"}
                      />
                    </Box>
                  </Grid>
                );
              })
            : null}
        </Grid>
      </Box>

      <CardActions
        disableSpacing
        sx={{ justifyContent: "space-between", marginInline: "1%" }}
        // marginInline={0.5}
      >
        <IconButton>
          <ChatBubbleOutlineIcon fontSize="small" />
          <Typography variant="body2">{replies}</Typography>
        </IconButton>
        <IconButton>
          <RepeatIcon fontSize="small" />
          <Typography variant="body2">{retweets}</Typography>
        </IconButton>
        <IconButton>
          <FavoriteIcon fontSize="small" />
          <Typography variant="body2">{favorites}</Typography>
        </IconButton>
        <IconButton>
          <VisibilityIcon fontSize="small" />
          <Typography variant="body2">{views}</Typography>
        </IconButton>
      </CardActions>
    </Card>
  );
}
