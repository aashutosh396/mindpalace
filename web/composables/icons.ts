// One icon family for the whole palace: Lucide (ISC license, open source).
// Room icons are stored by name; this map is the single source of truth.
import {
  Hash, MessageSquare, Code2, Globe, ShoppingBag, Wrench, Rocket, BookOpen,
  Briefcase, Database, Server, Smartphone, Palette, Camera, Music, Heart,
  Star, Zap, Shield, ShoppingCart, Mail, Bot, FlaskConical, Gamepad2,
  Landmark, Folder
} from 'lucide-vue-next'

export const ROOM_ICONS: Record<string, any> = {
  hash: Hash,
  'message-square': MessageSquare,
  code: Code2,
  globe: Globe,
  'shopping-bag': ShoppingBag,
  wrench: Wrench,
  rocket: Rocket,
  'book-open': BookOpen,
  briefcase: Briefcase,
  database: Database,
  server: Server,
  smartphone: Smartphone,
  palette: Palette,
  camera: Camera,
  music: Music,
  heart: Heart,
  star: Star,
  zap: Zap,
  shield: Shield,
  'shopping-cart': ShoppingCart,
  mail: Mail,
  bot: Bot,
  flask: FlaskConical,
  gamepad: Gamepad2,
  landmark: Landmark,
  folder: Folder
}

export function roomIcon(name?: string) {
  return ROOM_ICONS[name || 'hash'] || Hash
}
