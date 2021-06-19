export class TwitterUser {
  id: number | undefined;
  name: string | undefined;
  profile_image_url: string | undefined;
  screen_name: string | undefined;
  created_at: Date = new Date();
}
