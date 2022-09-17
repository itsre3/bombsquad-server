
# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING

import random
import ba
import _ba
from bastd.gameutils import SharedObjects
from bastd.actor import powerupbox
from bastd.actor.powerupbox import *
from bastd.actor import spaz
from bastd.actor.spazfactory import SpazFactory

if TYPE_CHECKING:
    from typing import Sequence, Union, Tuple, List, Any, Optional

apg = ba.app.config

powerup_config = {
        "triple_bombs": 0,
        "impact_bombs": 0,
        "sheild": 0,
        "ice_bombs": 0,
        "boxing_gloves": 0,
        "landmines": 0,
        "sticky_bombs": 0,
        "portal_bombs": 7,
        "curse": 0,
        "health": 3}

if "powerup" in ba.app.config:

    old_config = ba.app.config["powerup"]

    for setting in powerup_config:

        if setting not in old_config:

            ba.app.config["powerup"] = powerup_config

else:

    ba.app.config["powerup"] = powerup_config
ba.app.config.apply_and_commit()



main_config = {
    "powerupdroptime": 10}

if "main" in apg:
    old = apg["main"]
    for sett in main_config:
        if sett not in old:
            apg["main"] = main_config
else:
    apg["main"] = main_config
apg.apply_and_commit()

def get_new_powerup_distribution() -> Sequence[Tuple[str, int]]:
    """Standard set of powerups."""
    apg = ba.app.config
    return (('triple_bombs', apg["powerup"]["triple_bombs"]),
            ('ice_bombs', apg["powerup"]["ice_bombs"]),
            ('punch', apg["powerup"]["boxing_gloves"]),
            ('impact_bombs', apg["powerup"]["impact_bombs"]),
            ('land_mines', apg["powerup"]["landmines"]),
            ('sticky_bombs', apg["powerup"]["sticky_bombs"]),
            ('shield', apg["powerup"]["sheild"]),
            ('health', apg["powerup"]["health"]),
            ('curse', apg["powerup"]["curse"]),
            ('portal', apg["powerup"]["portal_bombs"]))




class new_powerup_box_factory(powerupbox.PowerupBoxFactory):
    def __init__(self):
        super().__init__()
        self.portal_tex = ba.gettexture("nub")
        
        self._powerupdist: List[str] = []
        for powerup, freq in get_new_powerup_distribution():
            for _i in range(int(freq)):
                self._powerupdist.append(powerup)
                
    def get_random_powerup_type(self,
                                forcetype: str = None,
                                excludetypes: List[str] = None) -> str:
        if excludetypes is None:
            excludetypes = []
        if forcetype:
            ptype = forcetype
        else:
            if self._lastpoweruptype == 'curse':
                ptype = 'health'
            else:
                while True:
                    ptype = self._powerupdist[random.randint(
                        0,
                        len(self._powerupdist) - 1)]
                    if ptype not in excludetypes:
                        break
        self._lastpoweruptype = ptype
        return ptype


    @classmethod
    def get(cls) -> PowerupBoxFactory:
        """Return a shared ba.PowerupBoxFactory object, creating if needed."""
        activity = ba.getactivity()
        if activity is None:
            raise ba.ContextError('No current activity.')
        factory = activity.customdata.get(cls._STORENAME)
        if factory is None:
            factory = activity.customdata[cls._STORENAME] = PowerupBoxFactory()
        assert isinstance(factory, PowerupBoxFactory)
        return factory

class new_PowerupBox(powerupbox.PowerupBox):
    """A box that grants a powerup.

    category: Gameplay Classes

    This will deliver a ba.PowerupMessage to anything that touches it
    which has the ba.PowerupBoxFactory.powerup_accept_material applied.
    """

    poweruptype: str
    """The string powerup type.  This can be 'triple_bombs', 'punch',
       'ice_bombs', 'impact_bombs', 'land_mines', 'sticky_bombs', 'shield',
       'health', or 'curse'."""

    node: ba.Node
    """The 'prop' ba.Node representing this box."""

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 poweruptype: str = 'triple_bombs',
                 expire: bool = True):
        """Create a powerup-box of the requested type at the given position.

        see ba.Powerup.poweruptype for valid type strings.
        """

        ba.Actor.__init__(self)
        shared = SharedObjects.get()
        factory = new_powerup_box_factory.get()
        self.poweruptype = poweruptype
        self._powersgiven = False

        if poweruptype == 'triple_bombs':
            tex = factory.tex_bomb
        elif poweruptype == 'punch':
            tex = factory.tex_punch
        elif poweruptype == 'ice_bombs':
            tex = factory.tex_ice_bombs
        elif poweruptype == 'impact_bombs':
            tex = factory.tex_impact_bombs
        elif poweruptype == 'land_mines':
            tex = factory.tex_land_mines
        elif poweruptype == 'sticky_bombs':
            tex = factory.tex_sticky_bombs
        elif poweruptype == 'shield':
            tex = factory.tex_shield
        elif poweruptype == 'health':
            tex = factory.tex_health
        elif poweruptype == 'curse':
            tex = factory.tex_curse
        elif poweruptype == 'portal':
            tex = factory.portal_tex
        else:
            raise ValueError('invalid poweruptype: ' + str(poweruptype))

        if len(position) != 3:
            raise ValueError('expected 3 floats for position')

        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'box',
                'position': position,
                'model': factory.model,
                'light_model': factory.model_simple,
                'shadow_size': 0.5,
                'color_texture': tex,
                'reflection': 'powerup',
                'reflection_scale': [1.0],
                'materials': (factory.powerup_material,
                              shared.object_material)
            })  # yapf: disable

        # Animate in.
        curve = ba.animate(self.node, 'model_scale', {0: 0, 0.14: 1.6, 0.2: 1})
        ba.timer(0.2, curve.delete)

        if expire:
            ba.timer(DEFAULT_POWERUP_INTERVAL - 2.5,
                     ba.WeakCall(self._start_flashing))
            ba.timer(DEFAULT_POWERUP_INTERVAL - 1.0,
                     ba.WeakCall(self.handlemessage, ba.DieMessage()))

    def _start_flashing(self) -> None:
        if self.node:
            self.node.flashing = True

    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired
        if isinstance(msg, ba.PowerupAcceptMessage):
            factory = new_powerup_box_factory.get()
            assert self.node
            if self.poweruptype == 'health':
                ba.playsound(factory.health_powerup_sound,
                             3,
                             position=self.node.position)
            ba.playsound(factory.powerup_sound, 3, position=self.node.position)
            self._powersgiven = True
            self.handlemessage(ba.DieMessage())

        elif isinstance(msg, powerupbox._TouchedMessage):
            if not self._powersgiven:
                node = ba.getcollision().opposingnode
                node.handlemessage(
                    ba.PowerupMessage(self.poweruptype, sourcenode=self.node))

        elif isinstance(msg, ba.DieMessage):
            if self.node:
                if msg.immediate:
                    self.node.delete()
                else:
                    ba.animate(self.node, 'model_scale', {0: 1, 0.1: 0})
                    ba.timer(0.1, self.node.delete)

        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())

        elif isinstance(msg, ba.HitMessage):
            # Don't die on punches (that's annoying).
            if msg.hit_type != 'punch':
                self.handlemessage(ba.DieMessage())
        else:
            return super().handlemessage(msg)
        return None



def new_spaz_handlemessage(self, msg: Any) -> Any:
  # pylint: disable=too-many-return-statements
  # pylint: disable=too-many-statements
  # pylint: disable=too-many-branches
    assert not self.expired

    if isinstance(msg, ba.PickedUpMessage):
        if self.node:
            self.node.handlemessage('hurt_sound')
            self.node.handlemessage('picked_up')
            # This counts as a hit.
        self._num_times_hit += 1

    elif isinstance(msg, ba.ShouldShatterMessage):
        # Eww; seems we have to do this in a timer or it wont work right.
        # (since we're getting called from within update() perhaps?..)
        # NOTE: should test to see if that's still the case.
        ba.timer(0.001, ba.WeakCall(self.shatter))

    elif isinstance(msg, ba.ImpactDamageMessage):
        # Eww; seems we have to do this in a timer or it wont work right.
        # (since we're getting called from within update() perhaps?..)
        ba.timer(0.001, ba.WeakCall(self._hit_self, msg.intensity))

    elif isinstance(msg, ba.PowerupMessage):
        if self._dead or not self.node:
            return True
        if self.pick_up_powerup_callback is not None:
            self.pick_up_powerup_callback(self)
        if msg.poweruptype == 'triple_bombs':
            tex = PowerupBoxFactory.get().tex_bomb
            self._flash_billboard(tex)
            self.set_bomb_count(3)
            if self.powerups_expire:
                self.node.mini_billboard_1_texture = tex
                t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_1_start_time = t_ms
                self.node.mini_billboard_1_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._multi_bomb_wear_off_flash_timer = (ba.Timer(
                    (POWERUP_WEAR_OFF_TIME - 2000),
                    ba.WeakCall(self._multi_bomb_wear_off_flash),
                    timeformat=ba.TimeFormat.MILLISECONDS))
                self._multi_bomb_wear_off_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    ba.WeakCall(self._multi_bomb_wear_off),
                    timeformat=ba.TimeFormat.MILLISECONDS))
        elif msg.poweruptype == 'land_mines':
            self.set_land_mine_count(min(self.land_mine_count + 3, 3))
        elif msg.poweruptype == 'impact_bombs':
            self.bomb_type = 'impact'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    ba.WeakCall(self._bomb_wear_off_flash),
                    timeformat=ba.TimeFormat.MILLISECONDS))
                self._bomb_wear_off_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    ba.WeakCall(self._bomb_wear_off),
                    timeformat=ba.TimeFormat.MILLISECONDS))
        elif msg.poweruptype == 'sticky_bombs':
            self.bomb_type = 'sticky'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    ba.WeakCall(self._bomb_wear_off_flash),
                    timeformat=ba.TimeFormat.MILLISECONDS))
                self._bomb_wear_off_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    ba.WeakCall(self._bomb_wear_off),
                    timeformat=ba.TimeFormat.MILLISECONDS))
        elif msg.poweruptype == 'punch':
            tex = PowerupBoxFactory.get().tex_punch
            self._flash_billboard(tex)
            self.equip_boxing_gloves()
            if self.powerups_expire and not self.default_boxing_gloves:
                self.node.boxing_gloves_flashing = False
                self.node.mini_billboard_3_texture = tex
                t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_3_start_time = t_ms
                self.node.mini_billboard_3_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._boxing_gloves_wear_off_flash_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    ba.WeakCall(self._gloves_wear_off_flash),
                    timeformat=ba.TimeFormat.MILLISECONDS))
                self._boxing_gloves_wear_off_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    ba.WeakCall(self._gloves_wear_off),
                    timeformat=ba.TimeFormat.MILLISECONDS))
        elif msg.poweruptype == 'shield':
            factory = SpazFactory.get()

            # Let's allow powerup-equipped shields to lose hp over time.
            self.equip_shields(decay=factory.shield_decay_rate > 0)
        elif msg.poweruptype == 'curse':
            self.curse()
        elif msg.poweruptype == 'ice_bombs':
            self.bomb_type = 'ice'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    ba.WeakCall(self._bomb_wear_off_flash),
                    timeformat=ba.TimeFormat.MILLISECONDS))
                self._bomb_wear_off_timer = (ba.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    ba.WeakCall(self._bomb_wear_off),
                    timeformat=ba.TimeFormat.MILLISECONDS))
        elif msg.poweruptype == 'health':
            if self._cursed:
                self._cursed = False

                # Remove cursed material.
                factory = SpazFactory.get()
                for attr in ['materials', 'roller_materials']:
                    materials = getattr(self.node, attr)
                    if factory.curse_material in materials:
                        setattr(
                            self.node, attr,
                            tuple(m for m in materials
                                  if m != factory.curse_material))
                self.node.curse_death_time = 0
            self.hitpoints = self.hitpoints_max
            self._flash_billboard(PowerupBoxFactory.get().tex_health)
            self.node.hurt = 0
            self._last_hit_time = None
            self._num_times_hit = 0

        elif msg.poweruptype == 'portal':
            ba.screenmessage("Pawriiiii")

        self.node.handlemessage('flash')
        if msg.sourcenode:
            msg.sourcenode.handlemessage(ba.PowerupAcceptMessage())
        return True

    elif isinstance(msg, ba.FreezeMessage):
        if not self.node:
            return None
        if self.node.invincible:
            ba.playsound(SpazFactory.get().block_sound,
                         1.0,
                         position=self.node.position)
            return None
        if self.shield:
            return None
        if not self.frozen:
            self.frozen = True
            self.node.frozen = True
            ba.timer(5.0, ba.WeakCall(self.handlemessage,
                                      ba.ThawMessage()))
            # Instantly shatter if we're already dead.
            # (otherwise its hard to tell we're dead)
            if self.hitpoints <= 0:
                self.shatter()

    elif isinstance(msg, ba.ThawMessage):
        if self.frozen and not self.shattered and self.node:
            self.frozen = False
            self.node.frozen = False

    elif isinstance(msg, ba.HitMessage):
        if not self.node:
            return None
        if self.node.invincible:
            ba.playsound(SpazFactory.get().block_sound,
                         1.0,
                         position=self.node.position)
            return True

        # If we were recently hit, don't count this as another.
        # (so punch flurries and bomb pileups essentially count as 1 hit)
        local_time = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(local_time, int)
        if (self._last_hit_time is None
                or local_time - self._last_hit_time > 1000):
            self._num_times_hit += 1
            self._last_hit_time = local_time

        mag = msg.magnitude * self.impact_scale
        velocity_mag = msg.velocity_magnitude * self.impact_scale
        damage_scale = 0.22

        # If they've got a shield, deliver it to that instead.
        if self.shield:
            if msg.flat_damage:
                damage = msg.flat_damage * self.impact_scale
            else:
                # Hit our spaz with an impulse but tell it to only return
                # theoretical damage; not apply the impulse.
                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1], msg.velocity[2], mag,
                    velocity_mag, msg.radius, 1, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
                damage = damage_scale * self.node.damage

            assert self.shield_hitpoints is not None
            self.shield_hitpoints -= int(damage)
            self.shield.hurt = (
                1.0 -
                float(self.shield_hitpoints) / self.shield_hitpoints_max)

            # Its a cleaner event if a hit just kills the shield
            # without damaging the player.
            # However, massive damage events should still be able to
            # damage the player. This hopefully gives us a happy medium.
            max_spillover = SpazFactory.get().max_shield_spillover_damage
            if self.shield_hitpoints <= 0:

                # FIXME: Transition out perhaps?
                self.shield.delete()
                self.shield = None
                ba.playsound(SpazFactory.get().shield_down_sound,
                             1.0,
                             position=self.node.position)

                # Emit some cool looking sparks when the shield dies.
                npos = self.node.position
                ba.emitfx(position=(npos[0], npos[1] + 0.9, npos[2]),
                          velocity=self.node.velocity,
                          count=random.randrange(20, 30),
                          scale=1.0,
                          spread=0.6,
                          chunk_type='spark')

            else:
                ba.playsound(SpazFactory.get().shield_hit_sound,
                             0.5,
                             position=self.node.position)

            # Emit some cool looking sparks on shield hit.
            assert msg.force_direction is not None
            ba.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 1.0,
                                msg.force_direction[1] * 1.0,
                                msg.force_direction[2] * 1.0),
                      count=min(30, 5 + int(damage * 0.005)),
                      scale=0.5,
                      spread=0.3,
                      chunk_type='spark')

            # If they passed our spillover threshold,
            # pass damage along to spaz.
            if self.shield_hitpoints <= -max_spillover:
                leftover_damage = -max_spillover - self.shield_hitpoints
                shield_leftover_ratio = leftover_damage / damage

                # Scale down the magnitudes applied to spaz accordingly.
                mag *= shield_leftover_ratio
                velocity_mag *= shield_leftover_ratio
            else:
                return True  # Good job shield!
        else:
            shield_leftover_ratio = 1.0

        if msg.flat_damage:
            damage = int(msg.flat_damage * self.impact_scale *
                         shield_leftover_ratio)
        else:
            # Hit it with an impulse and get the resulting damage.
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                msg.velocity[0], msg.velocity[1], msg.velocity[2], mag,
                velocity_mag, msg.radius, 0, msg.force_direction[0],
                msg.force_direction[1], msg.force_direction[2])

            damage = int(damage_scale * self.node.damage)
        self.node.handlemessage('hurt_sound')

        # Play punch impact sound based on damage if it was a punch.
        if msg.hit_type == 'punch':
            self.on_punched(damage)

            # If damage was significant, lets show it.
            if damage > 350:
                assert msg.force_direction is not None
                ba.show_damage_count('-' + str(int(damage / 10)) + '%',
                                     msg.pos, msg.force_direction)

            # Let's always add in a super-punch sound with boxing
            # gloves just to differentiate them.
            if msg.hit_subtype == 'super_punch':
                ba.playsound(SpazFactory.get().punch_sound_stronger,
                             1.0,
                             position=self.node.position)
            if damage > 500:
                sounds = SpazFactory.get().punch_sound_strong
                sound = sounds[random.randrange(len(sounds))]
            else:
                sound = SpazFactory.get().punch_sound
            ba.playsound(sound, 1.0, position=self.node.position)

            # Throw up some chunks.
            assert msg.force_direction is not None
            ba.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 0.5,
                                msg.force_direction[1] * 0.5,
                                msg.force_direction[2] * 0.5),
                      count=min(10, 1 + int(damage * 0.0025)),
                      scale=0.3,
                      spread=0.03)

            ba.emitfx(position=msg.pos,
                      chunk_type='sweat',
                      velocity=(msg.force_direction[0] * 1.3,
                                msg.force_direction[1] * 1.3 + 5.0,
                                msg.force_direction[2] * 1.3),
                      count=min(30, 1 + int(damage * 0.04)),
                      scale=0.9,
                      spread=0.28)

            # Momentary flash.
            hurtiness = damage * 0.003
            punchpos = (msg.pos[0] + msg.force_direction[0] * 0.02,
                        msg.pos[1] + msg.force_direction[1] * 0.02,
                        msg.pos[2] + msg.force_direction[2] * 0.02)
            flash_color = (1.0, 0.8, 0.4)
            light = ba.newnode(
                'light',
                attrs={
                    'position': punchpos,
                    'radius': 0.12 + hurtiness * 0.12,
                    'intensity': 0.3 * (1.0 + 1.0 * hurtiness),
                    'height_attenuated': False,
                    'color': flash_color
                })
            ba.timer(0.06, light.delete)

            flash = ba.newnode('flash',
                               attrs={
                                   'position': punchpos,
                                   'size': 0.17 + 0.17 * hurtiness,
                                   'color': flash_color
                               })
            ba.timer(0.06, flash.delete)

        if msg.hit_type == 'impact':
            assert msg.force_direction is not None
            ba.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 2.0,
                                msg.force_direction[1] * 2.0,
                                msg.force_direction[2] * 2.0),
                      count=min(10, 1 + int(damage * 0.01)),
                      scale=0.4,
                      spread=0.1)
        if self.hitpoints > 0:

            # It's kinda crappy to die from impacts, so lets reduce
            # impact damage by a reasonable amount *if* it'll keep us alive
            if msg.hit_type == 'impact' and damage > self.hitpoints:
                # Drop damage to whatever puts us at 10 hit points,
                # or 200 less than it used to be whichever is greater
                # (so it *can* still kill us if its high enough)
                newdamage = max(damage - 200, self.hitpoints - 10)
                damage = newdamage
            self.node.handlemessage('flash')

            # If we're holding something, drop it.
            if damage > 0.0 and self.node.hold_node:
                self.node.hold_node = None
            self.hitpoints -= damage
            self.node.hurt = 1.0 - float(
                self.hitpoints) / self.hitpoints_max

            # If we're cursed, *any* damage blows us up.
            if self._cursed and damage > 0:
                ba.timer(
                    0.05,
                    ba.WeakCall(self.curse_explode,
                                msg.get_source_player(ba.Player)))

            # If we're frozen, shatter.. otherwise die if we hit zero
            if self.frozen and (damage > 200 or self.hitpoints <= 0):
                self.shatter()
            elif self.hitpoints <= 0:
                self.node.handlemessage(
                    ba.DieMessage(how=ba.DeathType.IMPACT))

        # If we're dead, take a look at the smoothed damage value
        # (which gives us a smoothed average of recent damage) and shatter
        # us if its grown high enough.
        if self.hitpoints <= 0:
            damage_avg = self.node.damage_smoothed * damage_scale
            if damage_avg > 1000:
                self.shatter()

    elif isinstance(msg, spaz.BombDiedMessage):
        self.bomb_count += 1

    elif isinstance(msg, ba.DieMessage):
        wasdead = self._dead
        self._dead = True
        self.hitpoints = 0
        if msg.immediate:
            if self.node:
                self.node.delete()
        elif self.node:
            self.node.hurt = 1.0
            if self.play_big_death_sound and not wasdead:
                ba.playsound(SpazFactory.get().single_player_death_sound)
            self.node.dead = True
            ba.timer(2.0, self.node.delete)

    elif isinstance(msg, ba.OutOfBoundsMessage):
        # By default we just die here.
        self.handlemessage(ba.DieMessage(how=ba.DeathType.FALL))

    elif isinstance(msg, ba.StandMessage):
        self._last_stand_pos = (msg.position[0], msg.position[1],
                                msg.position[2])
        if self.node:
            self.node.handlemessage('stand', msg.position[0],
                                    msg.position[1], msg.position[2],
                                    msg.angle)

    elif isinstance(msg, spaz.CurseExplodeMessage):
        self.curse_explode()

    elif isinstance(msg, spaz.PunchHitMessage):
        if not self.node:
            return None
        node = ba.getcollision().opposingnode

        # Only allow one hit per node per punch.
        if node and (node not in self._punched_nodes):

            punch_momentum_angular = (self.node.punch_momentum_angular *
                                      self._punch_power_scale)
            punch_power = self.node.punch_power * self._punch_power_scale

            # Ok here's the deal:  we pass along our base velocity for use
            # in the impulse damage calculations since that is a more
            # predictable value than our fist velocity, which is rather
            # erratic. However, we want to actually apply force in the
            # direction our fist is moving so it looks better. So we still
            # pass that along as a direction. Perhaps a time-averaged
            # fist-velocity would work too?.. perhaps should try that.

            # If its something besides another spaz, just do a muffled
            # punch sound.
            if node.getnodetype() != 'spaz':
                sounds = SpazFactory.get().impact_sounds_medium
                sound = sounds[random.randrange(len(sounds))]
                ba.playsound(sound, 1.0, position=self.node.position)

            ppos = self.node.punch_position
            punchdir = self.node.punch_velocity
            vel = self.node.punch_momentum_linear

            self._punched_nodes.add(node)
            node.handlemessage(
                ba.HitMessage(
                    pos=ppos,
                    velocity=vel,
                    magnitude=punch_power * punch_momentum_angular * 110.0,
                    velocity_magnitude=punch_power * 40,
                    radius=0,
                    srcnode=self.node,
                    source_player=self.source_player,
                    force_direction=punchdir,
                    hit_type='punch',
                    hit_subtype=('super_punch' if self._has_boxing_gloves
                                 else 'default')))

            # Also apply opposite to ourself for the first punch only.
            # This is given as a constant force so that it is more
            # noticeable for slower punches where it matters. For fast
            # awesome looking punches its ok if we punch 'through'
            # the target.
            mag = -400.0
            if self._hockey:
                mag *= 0.5
            if len(self._punched_nodes) == 1:
                self.node.handlemessage('kick_back', ppos[0], ppos[1],
                                        ppos[2], punchdir[0], punchdir[1],
                                        punchdir[2], mag)
    elif isinstance(msg, spaz.PickupMessage):
        if not self.node:
            return None

        try:
            collision = ba.getcollision()
            opposingnode = collision.opposingnode
            opposingbody = collision.opposingbody
        except ba.NotFoundError:
            return True

        # Don't allow picking up of invincible dudes.
        try:
            if opposingnode.invincible:
                return True
        except Exception:
            pass

        # If we're grabbing the pelvis of a non-shattered spaz, we wanna
        # grab the torso instead.
        if (opposingnode.getnodetype() == 'spaz'
                and not opposingnode.shattered and opposingbody == 4):
            opposingbody = 1

        # Special case - if we're holding a flag, don't replace it
        # (hmm - should make this customizable or more low level).
        held = self.node.hold_node
        if held and held.getnodetype() == 'flag':
            return True

        # Note: hold_body needs to be set before hold_node.
        self.node.hold_body = opposingbody
        self.node.hold_node = opposingnode
    elif isinstance(msg, ba.CelebrateMessage):
        if self.node:
            self.node.handlemessage('celebrate', int(msg.duration * 1000))

    else:
        return ba.Actor.handlemessage(self, msg)
    return None

# ba_meta export plugin
class itsre3(ba.Plugin):
    def on_app_running(self):
        powerupbox.PowerupBoxFactory = new_powerup_box_factory
        powerupbox.PowerupBox.__init__ = new_PowerupBox.__init__
        spaz.Spaz.handlemessage = new_spaz_handlemessage