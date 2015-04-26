<?php
defined( '_JEXEC' ) or die( 'Restricted access' );
require_once( dirname(__FILE__).'/helper.php' );

$document = JFactory::getDocument();
$document->addScript('modules/mod_$LOW_NAME$/assets/js/script.js');
$document->addStyleSheet('modules/mod_$LOW_NAME$/assets/css/style.css');

$list = mod$FCUP_NAME$Helper::getList($params);

$moduleclass_sfx = htmlspecialchars($params->get('moduleclass_sfx'));
require JModuleHelper::getLayoutPath('mod_$LOW_NAME$', $params->get('layout', 'default'));