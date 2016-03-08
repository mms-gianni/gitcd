from gitcd.Exceptions import GitcdException
from gitcd.Config.File import File as ConfigFile
from gitcd.Interface.AbstractInterface import AbstractInterface
from gitcd.Interface.Cli import Cli
from gitcd.Cli.Command import Command as CliCommand

from pprint import pprint

class Gitcd(object):


  interface = False
  configFile = ConfigFile()
  cliCommand = CliCommand()

  featureMethods = {
    'start': 'featureStart',
    'test': 'featureTest',
    'review': 'featureReview',
    'finish': 'featureFinish',
    'deploy': 'featureDeploy'
  }

  def setInterface(self, interface: AbstractInterface):
    self.interface = interface

  def setConfigFilename(self, configFilename: str):
    self.configFile.setConfigFilename(configFilename)

  def loadConfig(self):
    # todo: maybe a warning if we are working with the default values
    self.configFile.load()

  def init(self):
    self.configFile.setMaster(
      self.interface.askFor("Branch name for production releases?",
      False,
      self.configFile.getMaster())
    )

    self.configFile.setFeature(
      self.interface.askFor("Branch name for feature development?",
      False,
      self.configFile.getFeature())
    )

    self.configFile.setTest(
      self.interface.askFor("Branch name for test releases?",
      False,
      self.configFile.getTest())
    )

    self.configFile.setTag(
      self.interface.askFor("Version tag prefix?",
      False,
      self.configFile.getTag())
    )

    self.configFile.write()
    pprint(self.configFile.config)


  
  def feature(self, command, branch):
    # remote upate
    self.update()

    # dispatch from mapping
    featureMethod = getattr(self, self.featureMethods[command])
    featureMethod(branch)

  def update(self):
    self.cliCommand.execute("git remote update")


  # maybe even take this in a own feature class
  def featureStart(self, branch: str):
    print("gitcd feature start")

  def featureTest(self, branch: str):
    print("gitcd feature test")

  def featureReview(self, branch: str):
    print("gitcd feature review")

  def featureFinish(self, branch: str):
    print("gitcd feature finish")

  def featureDeploy(self, branch: str):
    # todo: no branchname needed cause we are just tagging the master branch
    # and it should probably be called directly from feature finish
    print("gitcd feature deploy")

