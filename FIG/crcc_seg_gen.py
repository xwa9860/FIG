from gen import Gen
# from serp_concept import Universe


class CRCCSegGen(Gen):
  '''
  generator for CRCC(center reflector coolant/control rod channel segment)
  '''

  def parse(self, a_seg, type):
      if type=='s':
            CRCC_text = []
            for key, channel in a_seg.channels.items():
                channel.gen.set_univId(self.univ.id)
                CRCC_text.append('\n%%---channel\n')
                CRCC_text.append(channel.generate_output())

            for key in a_seg.sub_comps:
                subcomp = a_seg.sub_comps[key]
                CRCC_text.append('\n%%---%s\n'%key)
                for key2 in subcomp.comp_dict:
                    subcomp.comp_dict[key2].gen.set_univId(a_seg.channels.values()[0].fill.gen.univ.id)
                    CRCC_text.append('\n%%---%s\n'%key2)
                    CRCC_text.append(subcomp.comp_dict[key2].generate_output())
                CRCC_text.append(subcomp.comp_dict.values()[0].fill.generate_output())
      return ''.join(CRCC_text)
